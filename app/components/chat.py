import reflex as rx
from .question import question as qa
from app import style
from app.states.state import State

def chat() -> rx.Component:
    
    return rx.box(
        rx.foreach(State.chat_history, lambda msg: qa(msg[0], msg[1])), 
        margin_y="2em")
   