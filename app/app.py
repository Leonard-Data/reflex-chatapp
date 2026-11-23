"""ChatGPT-style chat UI: sidebar of conversations + streaming mock replies."""

import reflex as rx

from app.components.chat import chat_thread
from app.components.composer import composer
from app.components.sidebar import sidebar
from app.states.state import ChatState


def index() -> rx.Component:
    return rx.hstack(
        sidebar(),
        rx.vstack(
            chat_thread(),
            composer(),
            flex="1",
            height="100vh",
            width="100%",
            background_color="#212121",
            overflow="hidden",
            align="stretch",
            gap="0",
            spacing="0",
        ),
        width="100%",
        height="100vh",
        align="stretch",
        spacing="0",
        gap="0",
        on_mount=ChatState.load,
    )


app = rx.App()
app.add_page(index)
