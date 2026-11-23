import datetime

import reflex as rx
from sqlalchemy import Column, Integer
from sqlmodel import Field


def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)


class Conversation(rx.Model, table=True):
    title: str = "New chat"
    created_at: datetime.datetime = Field(default_factory=_now)
    updated_at: datetime.datetime = Field(default_factory=_now)


class Message(rx.Model, table=True):
    conversation_id: int = Field(
        sa_column=Column(Integer, index=True, nullable=False)
    )
    role: str = "user"  # "user" | "assistant"
    content: str = ""
    created_at: datetime.datetime = Field(default_factory=_now)
