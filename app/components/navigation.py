import reflex as rx
from app.state import ResumeState


def nav_button(text: str, tab_name: str) -> rx.Component:
    """A navigation tab button."""
    is_active = ResumeState.active_tab == tab_name
    return rx.el.button(
        text,
        on_click=lambda: ResumeState.set_active_tab(tab_name),
        class_name=rx.cond(
            is_active,
            "px-4 py-2 text-sm font-medium text-teal-700 bg-teal-50 rounded-lg",
            "px-4 py-2 text-sm font-medium text-gray-500 hover:text-gray-900 hover:bg-gray-100 rounded-lg",
        ),
        transition="all 0.2s ease-in-out",
    )


def navigation() -> rx.Component:
    """The main navigation component with tabs."""
    return rx.el.div(
        nav_button("Details", "details"),
        nav_button("Artifacts", "artifacts"),
        class_name="flex items-center p-1 space-x-1 bg-gray-100/50 rounded-xl border border-gray-200",
    )


def sticky_header() -> rx.Component:
    """A sticky header that appears on scroll."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span("Will Bricker", class_name="font-bold text-gray-800"),
                class_name="flex items-center",
            ),
            navigation(),
            class_name="flex items-center justify-between max-w-7xl mx-auto w-full px-8",
        ),
        class_name="fixed top-0 left-0 right-0 h-[60px] flex items-center bg-white/80 backdrop-blur-sm border-b border-gray-200 z-50",
    )