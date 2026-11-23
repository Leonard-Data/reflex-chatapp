"""Chat state: conversations + streaming mock replies, persisted in SQLite."""

import asyncio
import datetime
from typing import TypedDict

import reflex as rx
from sqlmodel import Session, delete, select

from app.models import Conversation, Message

CANNED_REPLY = (
    "I'm a mock assistant running fully offline. Your message was saved to "
    "SQLite, and this reply is streamed one character at a time. "
    "Try creating a new chat, switching conversations, or deleting one."
)


class ConversationView(TypedDict):
    id: int
    title: str


class MessageView(TypedDict):
    id: int
    role: str
    content: str


def _db() -> Session:
    return rx.model.session()


def _seed() -> None:
    """Insert mock conversations when the DB is empty."""
    rx.model.create_all()
    with _db() as session:
        if session.exec(select(Conversation)).first() is not None:
            return
        now = datetime.datetime.now(datetime.UTC)
        pairs = [
            ("weekend dinner ideas", "Any ideas for a quick dinner?", "Try a 15-minute lemon garlic pasta: boil spaghetti, toss with olive oil, lemon zest, garlic and parmesan."),
            ("explain recursion simply", "Explain recursion in one sentence.", "Recursion is when a function solves a problem by calling itself on a smaller version of the same problem."),
            ("python tips", "Give me one Python tip.", "Use `enumerate()` instead of `range(len(seq))` when you need both index and value."),
        ]
        for title, question, reply in pairs:
            conv = Conversation(title=title, created_at=now, updated_at=now)
            session.add(conv)
            session.commit()
            session.refresh(conv)
            session.add(Message(conversation_id=conv.id, role="user", content=question))
            session.add(Message(conversation_id=conv.id, role="assistant", content=reply))
            session.commit()


class ChatState(rx.State):
    conversations: list[ConversationView] = []
    messages: list[MessageView] = []
    current_id: int = 0
    draft: str = ""
    streaming: bool = False

    @rx.var
    def can_send(self) -> bool:
        return bool(self.draft.strip()) and not self.streaming

    def _load_messages(self) -> None:
        if not self.current_id:
            self.messages = []
            return
        with _db() as session:
            rows = session.exec(
                select(Message)
                .where(Message.conversation_id == self.current_id)
                .order_by(Message.id)
            ).all()
        self.messages = [
            MessageView(id=m.id, role=m.role, content=m.content) for m in rows
        ]

    def _load_conversations(self) -> None:
        with _db() as session:
            rows = session.exec(
                select(Conversation).order_by(Conversation.updated_at.desc())
            ).all()
        self.conversations = [
            ConversationView(id=c.id, title=c.title) for c in rows
        ]

    @rx.event
    def load(self):
        _seed()
        self._load_conversations()
        self._load_messages()

    @rx.event
    def select_conversation(self, conversation_id: int):
        self.current_id = conversation_id
        self._load_messages()

    @rx.event
    def new_chat(self):
        self.current_id = 0
        self.messages = []
        self.draft = ""

    @rx.event
    def delete_conversation(self, conversation_id: int):
        with _db() as session:
            session.exec(delete(Message).where(Message.conversation_id == conversation_id))
            session.exec(delete(Conversation).where(Conversation.id == conversation_id))
            session.commit()
        self._load_conversations()
        if self.current_id == conversation_id:
            self.current_id = 0
            self.messages = []

    @rx.event
    def set_draft(self, value: str):
        self.draft = value

    @rx.event
    async def send(self):
        text = self.draft.strip()
        if not text or self.streaming:
            return
        self.streaming = True
        self.draft = ""
        old_messages = self.messages
        now = datetime.datetime.now(datetime.UTC)

        with _db() as session:
            conv = session.get(Conversation, self.current_id) if self.current_id else None
            if conv is None:
                title = text if len(text) <= 40 else text[:40].rstrip() + "…"
                conv = Conversation(title=title, created_at=now, updated_at=now)
                session.add(conv)
                session.commit()
                session.refresh(conv)
                self.current_id = conv.id
            elif not session.exec(
                select(Message).where(Message.conversation_id == conv.id, Message.role == "user")
            ).first():
                conv.title = text if len(text) <= 40 else text[:40].rstrip() + "…"
            conv.updated_at = now
            session.add(Message(conversation_id=conv.id, role="user", content=text))
            session.add(conv)
            session.commit()

        base = [*old_messages, MessageView(id=-1, role="user", content=text)]
        self.messages = [*base, MessageView(id=-2, role="assistant", content="")]
        self._load_conversations()
        yield

        for i in range(1, len(CANNED_REPLY) + 1):
            await asyncio.sleep(0.015)
            self.messages = [*base, MessageView(id=-2, role="assistant", content=CANNED_REPLY[:i])]
            yield

        with _db() as session:
            session.add(Message(conversation_id=self.current_id, role="assistant", content=CANNED_REPLY))
            conv = session.get(Conversation, self.current_id)
            if conv is not None:
                conv.updated_at = datetime.datetime.now(datetime.UTC)
                session.add(conv)
            session.commit()
        self.streaming = False
        self._load_messages()
