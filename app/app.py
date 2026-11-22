"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from app.components.chat_popup import chat_popout
from rxconfig import config

class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        chat_popout()
    )


app = rx.App()
app.add_page(index)
