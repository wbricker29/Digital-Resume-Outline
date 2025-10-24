import os
import reflex as rx
import asyncio
from openai import OpenAI
from app.vector_db.chromadb_setup import search_vector_store, SearchResult
from typing import Generator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import os
import reflex as rx
import asyncio
import time
import uuid
from openai import OpenAI
from app.vector_db.chromadb_setup import search_vector_store, SearchResult
from typing import AsyncGenerator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
PROMPT_TEMPLATE = """
You are Will Bricker's AI assistant, designed to help recruiters, hiring managers, and professional contacts understand his qualifications. Your tone is professional, helpful, and concise.

Answer the user's question based *only* on the provided context. Do not make up information. If the context is insufficient, politely state that you cannot find the relevant information in the knowledge base.

When you use information from the context, you MUST cite the source. Use the 'section', 'company', 'title', or other metadata to create a clear citation, like `(Source: Experience at Company Inc.)` or `(Source: Core Competencies - Technical)`. Append citations at the end of the sentence or paragraph they support.

Conversation History:
{history}

Context from Knowledge Base:
{context}

User Question: {question}

Answer:
"""
GPT4O_INPUT_COST_PER_MIL = 2.5
GPT4O_OUTPUT_COST_PER_MIL = 10.0


def _format_search_results(results: list[SearchResult]) -> str:
    """Formats search results into a string for the LLM context."""
    context_str = ""
    for i, res in enumerate(results):
        metadata_str = ", ".join(
            (f"{k}: {v}" for k, v in res.get("metadata", {}).items() if v)
        )
        context_str += (
            f"Chunk {i + 1} (Source: {metadata_str}):\\n{res['document']}\\n\\n"
        )
    return context_str


async def answer_question_with_rag(
    question: str, history: list[str]
) -> AsyncGenerator[str, None]:
    """Handles the RAG pipeline: retrieval, context assembly, and generation."""
    correlation_id = uuid.uuid4()
    start_time = time.perf_counter()
    logger.info(f"[correlation_id={correlation_id}] Query received: {question}")
    try:
        retrieval_start = time.perf_counter()
        search_results = search_vector_store(query_text=question, n_results=5)
        retrieval_end = time.perf_counter()
        retrieval_latency = (retrieval_end - retrieval_start) * 1000
        filtered_results = [
            res for res in search_results if res.get("distance", 1.0) < 0.7
        ]
        distances = [r.get("distance", 0.0) for r in filtered_results]
        if distances:
            dist_stats = f"min={min(distances):.4f}, max={max(distances):.4f}, avg={sum(distances) / len(distances):.4f}"
        else:
            dist_stats = "N/A"
        logger.info(
            f"[correlation_id={correlation_id}] Vector retrieval: {len(filtered_results)}/{len(search_results)} chunks in {retrieval_latency:.2f}ms, distances: {dist_stats}"
        )
        if not filtered_results:
            yield "I couldn't find any specific information about that in my knowledge base. Could you rephrase your question?"
            return
        context_str = _format_search_results(filtered_results)
        history_str = """
""".join(history[-10:])
        prompt = PROMPT_TEMPLATE.format(
            history=history_str, context=context_str, question=question
        )
        logger.info(f"[correlation_id={correlation_id}] Starting LLM generation...")
        generation_start = time.perf_counter()
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional AI assistant."},
                {"role": "user", "content": prompt},
            ],
            stream=True,
            temperature=0.2,
            stream_options={"include_usage": True},
        )
        response_content = ""
        first_token_time = None
        for chunk in stream:
            if (
                first_token_time is None
                and chunk.choices
                and chunk.choices[0].delta.content
            ):
                first_token_time = time.perf_counter()
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                response_content += content
                yield content
                await asyncio.sleep(0)
            if chunk.usage:
                generation_end = time.perf_counter()
                input_tokens = chunk.usage.prompt_tokens
                output_tokens = chunk.usage.completion_tokens
                total_tokens = chunk.usage.total_tokens
                cost = (
                    input_tokens / 1000000 * GPT4O_INPUT_COST_PER_MIL
                    + output_tokens / 1000000 * GPT4O_OUTPUT_COST_PER_MIL
                )
                gen_latency = (generation_end - generation_start) * 1000
                first_token_latency = (
                    (first_token_time - generation_start) * 1000
                    if first_token_time
                    else -1
                )
                logger.info(
                    f"[correlation_id={correlation_id}] LLM generation complete: {input_tokens} input + {output_tokens} output = {total_tokens} tokens, cost=${cost:.6f}, latency={gen_latency:.2f}ms (first_token: {first_token_latency:.2f}ms)"
                )
    except Exception as e:
        logger.exception(
            f"[correlation_id={correlation_id}] Error in RAG pipeline: {e}"
        )
        yield """

Sorry, I encountered an unexpected error while processing your request. Please try again later."""
    finally:
        end_time = time.perf_counter()
        total_latency = (end_time - start_time) * 1000
        logger.info(
            f"[correlation_id={correlation_id}] Request complete: {total_latency:.2f}ms end-to-end, response length={len(response_content)} chars"
        )
        yield """

Sorry, I encountered an unexpected error while processing your request. Please try again later."""