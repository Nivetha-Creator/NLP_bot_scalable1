from sqlalchemy.orm import Session

from src.nlp_bot_scalable.database.models import ChatMessage

def get_chat_history(db: Session):
    return (
        db.query(ChatMessage)
        .order_by(ChatMessage.id.desc())
        .all()
    )

def save_chat(
    db: Session,
    user_message: str,
    bot_response: str,
    intent: str | None = None,
):
    chat = ChatMessage(
        user_message=user_message,
        bot_response=bot_response,
        intent=intent,
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat