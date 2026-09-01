from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_message: Mapped[str] = mapped_column(Text)

    bot_response: Mapped[str] = mapped_column(Text)

    intent: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )