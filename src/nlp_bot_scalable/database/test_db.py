from sqlalchemy import select

from src.config.database import SessionLocal
from src.nlp_bot_scalable.database.models import ChatMessage


def test_database():
    db = SessionLocal()

    chats = db.execute(
        select(ChatMessage)
    ).scalars().all()

    for chat in chats:
        print(
            f"ID: {chat.id} | "
            f"User: {chat.user_message} | "
            f"Bot: {chat.bot_response} | "
            f"Intent: {chat.intent}"
        )

    db.close()


if __name__ == "__main__":
    test_database()