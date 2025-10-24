import reflex as rx
from typing import Literal

ActiveTab = Literal["details", "artifacts"]


class ResumeState(rx.State):
    """The state for the resume app."""

    active_tab: ActiveTab = "details"
    active_section: str = "intro"
    chat_input: str = ""
    messages: list[str] = []

    @rx.event
    def set_active_tab(self, tab: ActiveTab):
        """Set the active navigation tab."""
        self.active_tab = tab
        section_id = "about" if tab == "details" else "artifacts"
        return ResumeState.scroll_to(section_id)

    @rx.event
    def scroll_to(self, section_id: str):
        """Scroll to a specific section."""
        return rx.call_script(
            f"document.getElementById('{section_id}').scrollIntoView({{behavior: 'smooth'}})"
        )

    @rx.event
    def handle_chat_submit(self, form_data: dict[str, str]):
        """Handle chat submission."""
        message = form_data.get("chat_input", "").strip()
        if message:
            self.messages.append(message)
            self.chat_input = ""