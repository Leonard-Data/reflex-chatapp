import reflex as rx

from app.states.state import ChatState


def composer() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text_area(
                value=ChatState.draft,
                on_change=ChatState.set_draft,
                placeholder="Message ChatGPT…",
                background="transparent",
                border="none",
                outline="none",
                resize="none",
                width="100%",
                min_height="44px",
                padding="0.6em 0.4em",
                color="#ececec",
                font_size="0.95rem",
                _placeholder={"color": "#8e8e8e"},
            ),
            rx.icon_button(
                rx.icon("arrow-up", size=18),
                on_click=ChatState.send,
                disabled=~ChatState.can_send,
                border_radius="full",
                background_color=rx.cond(ChatState.can_send, "#ececec", "#2f2f2f"),
                color=rx.cond(ChatState.can_send, "#171717", "#8e8e8e"),
                cursor="pointer",
                flex_shrink="0",
                size="2",
            ),
            align="end",
            width="100%",
            gap="0.5em",
            background_color="#212121",
            border="1px solid #3a3a3a",
            border_radius="1.5em",
            padding="0.5em 0.5em 0.5em 0.75em",
            box_shadow="0 4px 16px rgba(0,0,0,0.3)",
        ),
        flex_shrink="0",
        width="100%",
        max_width="48em",
        margin="0 auto",
        padding="1em 1em 1.5em",
    )
