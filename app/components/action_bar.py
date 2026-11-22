import reflex as rx
from app.states.state import State
from app import style


def action_bar() -> rx.Component:
    return rx.hstack    (
        rx.input(placeholder="Type your message...", 
                value=State.question,
                width="100%",
                style=style.input_style, 
                on_change=State.set_question),
        rx.button("Ask", 
                  color_scheme="blue", 
                  style=style.button_style, 
                  on_click=State.answer),
        margin_y="2em",
    )