from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.config.database import SessionLocal
from src.nlp_bot_scalable.database.chat_repository import get_chat_history
from src.nlp_bot_scalable.services.chat_service import ChatService


app = FastAPI(
    title="NLP Chatbot API",
    description="Scalable NLP Chatbot API",
    version="1.0.0"
)


# Allow frontend to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create chatbot service
chat_service = ChatService()


# Request schema
class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        description="Message to send to the chatbot"
    )


# Response schema
class ChatResponse(BaseModel):
    intent: str | None
    probability: str | None
    response: str


# Chat history response schema
class ChatHistoryResponse(BaseModel):
    id: int
    user_message: str
    bot_response: str
    intent: str | None


# Database dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "NLP Chatbot API is running!"
    }


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    return chat_service.chat(
        db,
        request.message
    )


# Chat history endpoint
@app.get(
    "/chat/history",
    response_model=list[ChatHistoryResponse]
)
def chat_history(
    db: Session = Depends(get_db)
):
    return get_chat_history(db)