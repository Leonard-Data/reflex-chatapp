import reflex as rx
from app import style
from app.components.action_bar import action_bar
from app.components.chat import chat

def chat_popout() -> rx.Component:
    return rx.popover.root(
        rx.popover.trigger(
            rx.icon_button("chat", color_scheme="blue", style=style.button_style),
        ),
        rx.popover.content(
            rx.container(
                chat(),
                action_bar(),
            )   
        )
    )