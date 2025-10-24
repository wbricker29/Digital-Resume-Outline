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
    def set_active_section(self, section_id: str):
        """Set the active section and update tab."""
        self.active_section = section_id
        if section_id in ["intro", "about"]:
            self.active_tab = "details"
        else:
            self.active_tab = "artifacts"

    @rx.event
    def on_load_observers(self):
        """Create intersection observers for all sections."""
        return rx.call_script(
            "createIntersectionObservers(['intro', 'about', 'artifacts'])"
        )

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