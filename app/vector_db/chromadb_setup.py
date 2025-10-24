import reflex as rx
import chromadb
import yaml
from pathlib import Path
from typing import Any, TypedDict, cast
from app.vector_db.yaml_parser import parse_reference_yaml_to_chunks
import logging

CHROMA_PATH = str(Path.cwd() / ".chroma_db")
COLLECTION_NAME = "resume_knowledge"


def get_vector_store() -> chromadb.Collection:
    """Get or create the ChromaDB vector store collection."""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )
    return collection


def initialize_vector_store():
    """Initialize and populate the vector store if it's empty."""
    collection = get_vector_store()
    if collection.count() == 0:
        print("Vector store is empty. Initializing with content from reference.yaml...")
        try:
            reference_path = Path.cwd() / "assets" / "reference.yaml"
            with open(reference_path, "r") as f:
                reference_data = yaml.safe_load(f)
            chunks = parse_reference_yaml_to_chunks(reference_data)
            if not chunks:
                print("Warning: No chunks were parsed from reference.yaml.")
                return
            ids = [chunk["id"] for chunk in chunks]
            documents = [chunk["content"] for chunk in chunks]
            metadatas = [chunk["metadata"] for chunk in chunks]
            collection.add(ids=ids, documents=documents, metadatas=metadatas)
            print(
                f"Successfully added {len(ids)} chunks to the '{COLLECTION_NAME}' collection."
            )
        except Exception as e:
            logging.exception(f"Error initializing vector store: {e}")


class SearchResult(TypedDict):
    id: str
    document: str
    metadata: dict[str, str]
    distance: float


def search_vector_store(query_text: str, n_results: int = 5) -> list[SearchResult]:
    """Search the vector store for relevant documents."""
    collection = get_vector_store()
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )
    flat_results = []
    if results and results["ids"] and results["ids"][0]:
        ids = results["ids"][0]
        documents = results["documents"][0] if results["documents"] else [""] * len(ids)
        metadatas = results["metadatas"][0] if results["metadatas"] else [{}] * len(ids)
        distances = (
            results["distances"][0] if results["distances"] else [0.0] * len(ids)
        )
        for i in range(len(ids)):
            flat_results.append(
                {
                    "id": ids[i],
                    "document": documents[i],
                    "metadata": cast(dict[str, str], metadatas[i]),
                    "distance": distances[i],
                }
            )
    return flat_results