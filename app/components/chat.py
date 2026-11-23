import reflex as rx

from app.states.state import ChatState


def user_bubble(message: rx.Var) -> rx.Component:
    return rx.box(
        rx.box(
            message["content"],
            background_color="#303030",
            color="#ececec",
            padding="0.75em 1em",
            border_radius="1.25em",
            max_width="36em",
            white_space="pre-wrap",
            word_break="break-word",
            font_size="0.95rem",
            line_height="1.6",
        ),
        display="flex",
        justify_content="flex-end",
        width="100%",
        padding="0.5em 0",
    )


def assistant_bubble(message: rx.Var) -> rx.Component:
    return rx.hstack(
        rx.el.div(
            "AI",
            width="28px",
            height="28px",
            flex_shrink="0",
            border_radius="full",
            background_color="#10a37f",
            color="white",
            font_size="0.7rem",
            font_weight="600",
            display="flex",
            align_items="center",
            justify_content="center",
            margin_top="0.35em",
        ),
        rx.box(
            message["content"],
            color="#ececec",
            white_space="pre-wrap",
            word_break="break-word",
            font_size="0.95rem",
            line_height="1.7",
            flex="1",
            min_width="0",
        ),
        width="100%",
        align_items="flex-start",
        gap="0.85em",
        padding="1em 0",
        border_bottom="1px solid #2f2f2f",
    )


def chat_thread() -> rx.Component:
    return rx.box(
        rx.cond(
            ChatState.messages,
            rx.box(
                rx.foreach(
                    ChatState.messages,
                    lambda m: rx.cond(
                        m["role"] == "user",
                        user_bubble(m),
                        assistant_bubble(m),
                    ),
                ),
                rx.cond(
                    ChatState.streaming,
                    rx.text("▍", color="#10a37f", font_size="0.9rem"),
                ),
                width="100%",
                max_width="48em",
                margin="0 auto",
                padding="1em 1em 8em",
            ),
            rx.center(
                rx.vstack(
                    rx.heading("What can I help with?", size="7", color="#ececec"),
                    rx.text(
                        "Mock ChatGPT clone — replies are canned and stored in SQLite.",
                        color="#8e8e8e",
                        font_size="0.9rem",
                    ),
                    gap="0.75em",
                    align="center",
                ),
                height="100%",
                width="100%",
            ),
        ),
        flex="1",
        overflow_y="auto",
        width="100%",
    )
