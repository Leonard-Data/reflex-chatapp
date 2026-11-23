import reflex as rx

from app.states.state import ChatState

ROW = dict(
    align_items="center",
    gap="0.5em",
    padding="0.5em 0.6em",
    border_radius="0.5em",
    cursor="pointer",
    color="#ececec",
    font_size="0.875rem",
    width="100%",
)


def conversation_row(c: rx.Var) -> rx.Component:
    return rx.hstack(
        rx.text(c["title"], flex="1", overflow="hidden", text_overflow="ellipsis", white_space="nowrap"),
        rx.button(
            rx.icon("trash-2", size=14),
            on_click=ChatState.delete_conversation(c["id"]),
            variant="ghost",
            color="inherit",
            flex_shrink="0",
            opacity="0.6",
            _hover={"opacity": "1"},
        ),
        on_click=ChatState.select_conversation(c["id"]),
        **ROW,
        background_color=rx.cond(ChatState.current_id == c["id"], "#2f2f2f", "transparent"),
        _hover={"background_color": rx.cond(ChatState.current_id == c["id"], "#2f2f2f", "#212121")},
    )


def sidebar() -> rx.Component:
    return rx.vstack(
        rx.button(
            rx.hstack(rx.icon("pencil", size=16), rx.text("New chat"), align="center", gap="0.5em"),
            on_click=ChatState.new_chat,
            width="100%",
            justify="flex-start",
            padding="0.75em 1em",
            border="1px solid #444",
            border_radius="0.75em",
            background="transparent",
            color="#ececec",
            cursor="pointer",
            _hover={"background_color": "#2f2f2f"},
        ),
        rx.box(
            rx.foreach(ChatState.conversations, conversation_row),
            overflow_y="auto",
            flex="1",
            width="100%",
            margin_top="0.75em",
        ),
        width="256px",
        flex_shrink="0",
        height="100vh",
        padding="0.75em",
        background_color="#171717",
        border_right="1px solid #2f2f2f",
    )
