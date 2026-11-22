import reflex as rx
from app import style

def question(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(question, style=style.question_style, text_align="right"),
        rx.box(answer, style=style.answer_style, text_align="left"),
        margin_y="1em",
        width="100%",
    )