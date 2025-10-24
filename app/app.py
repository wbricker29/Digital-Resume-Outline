import reflex as rx
from app.state import ResumeState
from app.components.sections import intro_section, about_section, artifacts_section
from app.components.navigation import sticky_header
from app.utils import intersection_observer


def index() -> rx.Component:
    """The main page of the resume."""
    return rx.el.div(
        sticky_header(),
        rx.el.main(
            intro_section(),
            about_section(),
            artifacts_section(),
            class_name="pt-[60px]",
        ),
        on_mount=ResumeState.on_load_observers(),
        class_name="font-['Inter'] bg-white",
        style={"scroll-behavior": "smooth"},
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
        intersection_observer(),
    ],
)
app.add_page(index, title="Will Bricker - Digital Resume")