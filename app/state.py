import reflex as rx
from typing import Literal
from app.vector_db.chromadb_setup import initialize_vector_store

ActiveTab = Literal["intro", "details", "artifacts"]


class ResumeState(rx.State):
    """The state for the resume app."""

    active_tab: ActiveTab = "intro"

    @rx.event
    def on_load(self):
        """Initialize the vector store on app load."""
        initialize_vector_store()

    @rx.event
    def set_active_tab(self, tab: ActiveTab):
        """Set the active navigation tab."""
        self.active_tab = tab
        if tab == "intro":
            section_id = "intro"
        elif tab == "details":
            section_id = "about"
        else:
            section_id = "artifacts"
        return ResumeState.scroll_to(section_id)

    @rx.event
    def scroll_to(self, section_id: str):
        """Scroll to a specific section."""
        return rx.call_script(
            f"document.getElementById('{section_id}').scrollIntoView({{behavior: 'smooth'}})"
        )