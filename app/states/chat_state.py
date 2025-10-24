import reflex as rx
from app.vector_db.chromadb_setup import search_vector_store


class ChatState(rx.State):
    """State for the chat component."""

    chat_input: str = ""
    messages: list[str] = []

    @rx.event
    def handle_chat_submit(self, form_data: dict[str, str]):
        """Handle chat submission."""
        message = form_data.get("chat_input", "").strip()
        if message:
            self.messages.append(f"You: {message}")
            yield
            self.chat_input = ""
            search_results = search_vector_store(query_text=message, n_results=3)
            if search_results:
                context = """
""".join([res["document"] for res in search_results])
                response = f"AI: (Context Found)\n{context[:500]}..."
                self.messages.append(response)
            else:
                self.messages.append("AI: I couldn't find any relevant information.")