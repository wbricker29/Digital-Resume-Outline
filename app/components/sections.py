import reflex as rx
from app.state import ResumeState
from app.states.chat_state import ChatState
from app.components.navigation import navigation
from app.content import (
    intro_content,
    about_content,
    writing_links,
    social_links,
    media_links,
    portfolio_links,
)


def scroll_indicator(target_id: str) -> rx.Component:
    """A scroll down indicator button."""
    return rx.el.button(
        rx.el.div(
            rx.el.span("Learn More", class_name="text-sm font-medium text-gray-500"),
            rx.icon(
                "arrow-down", size=16, class_name="text-gray-500 ml-2 animate-bounce"
            ),
            class_name="flex items-center",
        ),
        on_click=lambda: ResumeState.scroll_to(target_id),
        class_name="mt-12 p-2 rounded-lg hover:bg-gray-100 transition-colors",
    )


def chat_message(text: str) -> rx.Component:
    """A chat message bubble."""
    is_user_message = text.startswith("You: ")
    display_text = rx.cond(is_user_message, text[5:], text[4:])
    return rx.el.div(
        rx.el.p(
            display_text,
            class_name=rx.cond(
                is_user_message,
                "text-sm text-white",
                "text-sm text-gray-700 whitespace-pre-wrap",
            ),
        ),
        class_name=rx.cond(
            is_user_message,
            "bg-teal-500 rounded-lg px-4 py-2 self-end max-w-lg",
            "bg-gray-200 rounded-lg px-4 py-2 self-start max-w-lg",
        ),
    )


def intro_section() -> rx.Component:
    """The introductory section of the resume."""
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    intro_content["name"],
                    class_name="text-5xl font-bold text-gray-800 mt-16",
                ),
                rx.el.div(
                    rx.el.h2(
                        intro_content["welcome_title"],
                        class_name="text-lg font-semibold text-gray-700",
                    ),
                    rx.el.p(intro_content["welcome_text"], class_name="text-gray-600"),
                    class_name="mt-8 space-y-2 text-base font-medium",
                ),
                rx.el.div(
                    rx.el.h2(
                        intro_content["current_title"],
                        class_name="text-lg font-semibold text-gray-700 mt-8",
                    ),
                    rx.el.ul(
                        rx.foreach(
                            intro_content["current_activities"],
                            lambda item: rx.el.li(f"- {item}"),
                        ),
                        class_name="space-y-1 text-gray-600 list-none",
                    ),
                    class_name="mt-2 space-y-4 text-base font-medium",
                ),
                rx.el.button(
                    "Contact Me",
                    class_name="mt-12 px-6 py-3 bg-teal-500 text-white font-semibold rounded-xl hover:bg-teal-600 transition-colors shadow-sm",
                ),
                scroll_indicator("about"),
                class_name="flex flex-col items-start h-full justify-center lg:col-span-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Ask me anything about my experience or projects.",
                            class_name="text-center text-sm text-gray-500",
                        ),
                        rx.foreach(ChatState.messages, chat_message),
                        class_name="flex-grow flex flex-col p-4 space-y-4 overflow-y-auto",
                    ),
                    rx.el.form(
                        rx.el.input(
                            name="chat_input",
                            placeholder="Type your question...",
                            class_name="w-full px-4 py-2 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400",
                            key=ChatState.chat_input,
                            default_value=ChatState.chat_input,
                        ),
                        rx.el.button(
                            rx.icon("arrow-up", size=16),
                            type="submit",
                            class_name="absolute right-3 top-1/2 -translate-y-1/2 p-2 bg-teal-500 text-white rounded-md hover:bg-teal-600",
                        ),
                        on_submit=ChatState.handle_chat_submit,
                        reset_on_submit=True,
                        class_name="relative p-4 border-t border-gray-200",
                    ),
                    class_name="flex flex-col h-[500px] lg:h-full w-full bg-gray-100/80 rounded-2xl border border-gray-200 shadow-sm",
                ),
                class_name="lg:flex items-center justify-center lg:col-span-4 h-full py-12",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-10 gap-16 max-w-7xl mx-auto px-8 h-full",
        ),
        id="intro",
        class_name="w-full flex items-center justify-center bg-gray-50/50 pt-16 lg:pt-0 min-h-screen py-12 lg:py-0",
    )


def about_section() -> rx.Component:
    """The about section."""
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    about_content["experience_title"],
                    class_name="text-3xl font-bold text-gray-800",
                ),
                rx.el.p(
                    about_content["experience_text"],
                    class_name="mt-6 text-gray-600 font-medium",
                ),
                scroll_indicator("artifacts"),
                class_name="flex flex-col items-start justify-center h-full",
            ),
            rx.el.div(
                rx.el.h2(
                    about_content["philosophy_title"],
                    class_name="text-3xl font-bold text-gray-800",
                ),
                rx.el.p(
                    about_content["philosophy_text"],
                    class_name="mt-6 text-gray-600 font-medium",
                ),
                rx.el.a(
                    rx.el.button(
                        rx.icon("download", size=16, class_name="mr-2"),
                        "Download Resume",
                        class_name="mt-8 px-5 py-2.5 border border-gray-300 text-gray-700 font-semibold rounded-xl hover:bg-gray-100 transition-colors flex items-center",
                    ),
                    href=about_content["resume_url"],
                    download=True,
                ),
                class_name="flex flex-col items-start justify-center h-full",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-16 max-w-7xl mx-auto px-8 h-full",
        ),
        id="about",
        class_name="min-h-screen w-full flex items-center justify-center bg-white py-12 lg:py-0",
    )


def link_card(icon_name: str, title: str, href: str) -> rx.Component:
    """A card for external links."""
    return rx.el.a(
        rx.el.div(
            rx.icon(icon_name, size=20, class_name="text-gray-500"),
            rx.el.span(title, class_name="font-semibold text-gray-800"),
            rx.icon(
                "arrow-up-right",
                size=16,
                class_name="text-gray-400 group-hover:text-teal-600 transition-colors",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        href=href,
        is_external=True,
        class_name="group flex items-center p-4 bg-white rounded-xl border border-gray-200 hover:border-teal-300 hover:shadow-sm transition-all duration-200",
    )


def social_link(icon_name: str, href: str) -> rx.Component:
    """A social media icon link."""
    return rx.el.a(
        rx.icon(
            icon_name,
            size=24,
            class_name="text-gray-500 hover:text-teal-600 transition-colors",
        ),
        href=href,
        is_external=True,
    )


def artifacts_section() -> rx.Component:
    """The artifacts section with writings, social media, media, and resources."""
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2("Writing", class_name="text-xl font-bold text-gray-800 mb-6"),
                rx.el.div(
                    rx.foreach(
                        writing_links,
                        lambda link: link_card(
                            link["icon"], link["title"], link["href"]
                        ),
                    ),
                    class_name="space-y-4",
                ),
                rx.el.h2(
                    "Socials", class_name="text-xl font-bold text-gray-800 mt-12 mb-6"
                ),
                rx.el.div(
                    rx.foreach(
                        social_links,
                        lambda link: social_link(link["icon"], link["href"]),
                    ),
                    class_name="flex items-center space-x-6",
                ),
                class_name="h-full flex flex-col justify-center",
            ),
            rx.el.div(
                rx.el.h2("Media", class_name="text-xl font-bold text-gray-800 mb-6"),
                rx.el.div(
                    rx.foreach(
                        media_links,
                        lambda link: link_card(
                            link["icon"], link["title"], link["href"]
                        ),
                    ),
                    class_name="space-y-4",
                ),
                rx.el.h2(
                    "Portfolio Resources",
                    class_name="text-xl font-bold text-gray-800 mt-12 mb-6",
                ),
                rx.el.div(
                    rx.foreach(
                        portfolio_links,
                        lambda link: link_card(
                            link["icon"], link["title"], link["href"]
                        ),
                    ),
                    class_name="space-y-4",
                ),
                class_name="h-full flex flex-col justify-center",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-x-16 gap-y-12 max-w-7xl mx-auto px-8 h-full py-12 lg:py-0",
        ),
        id="artifacts",
        class_name="min-h-screen w-full flex items-center justify-center bg-gray-50/50",
    )