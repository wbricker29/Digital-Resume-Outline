import reflex as rx
import asyncio
import logging
from app.services.rag_service import answer_question_with_rag

logger = logging.getLogger(__name__)


class ChatState(rx.State):
    """State for the chat component."""

    messages: list[str] = [
        "AI: Hi! I'm Will's AI assistant. Ask me anything about his experience, skills, or projects."
    ]
    is_streaming: bool = False
    is_thinking: bool = False
    chat_input: str = ""

    @rx.var
    def get_message_count(self) -> int:
        return len(self.messages)

    @rx.event
    async def handle_chat_submit(self, form_data: dict[str, str]):
        """Handle chat submission and stream response."""
        message = form_data.get("chat_input", "").strip()
        if not message:
            return
        self.messages.append(f"You: {message}")
        self.is_thinking = True
        yield
        self.is_streaming = True
        self.messages.append("AI: ")
        yield
        try:
            stream = answer_question_with_rag(message, self.messages[:-2])
            async for chunk in stream:
                if chunk:
                    if self.is_thinking:
                        self.is_thinking = False
                    self.messages[-1] += chunk
                    yield
        except Exception as e:
            logger.exception(f"RAG Error in ChatState: {e}")
            self.messages[-1] += """
Sorry, an error occurred. Please try again."""
            yield
        finally:
            self.is_thinking = False
            self.is_streaming = False