from sqlalchemy.orm import Session

from src.nlp_bot_scalable.database.chat_repository import save_chat
from src.nlp_bot_scalable.database.models import ChatMessage
from src.nlp_bot_scalable.nlp.predictor import ChatbotPredictor


class ChatService:

    def __init__(self):
        self.predictor = ChatbotPredictor()

    def chat(self, db: Session, user_message: str):

        message = user_message.lower().strip()

        # Get the previous conversation
        previous_chat = (
            db.query(ChatMessage)
            .order_by(ChatMessage.id.desc())
            .first()
        )

        result = None

        # ==================================================
        # 1. THANK YOU / GRATITUDE
        # ==================================================

        gratitude_messages = [
            "thanks",
            "thank you",
            "thanks a lot",
            "thank you so much",
            "thx",
            "ty",
            "appreciate it",
            "appreciate that",
        ]

        if message in gratitude_messages:

            result = {
                "intent": "gratitude",
                "probability": "1.0",
                "response": "You're very welcome! 😊 Is there anything else I can help you with?"
            }

        # ==================================================
        # 2. GOODBYE
        # ==================================================

        elif message in ["bye", "goodbye", "see you", "see ya", "talk to you later"]:

            result = {
                "intent": "goodbye",
                "probability": "1.0",
                "response": "Goodbye! 👋 Have a great day!"
            }

        # ==================================================
        # 3. RESPONSE TO "HOW ARE YOU?"
        # ==================================================

        elif previous_chat:

            previous_bot_message = previous_chat.bot_response.lower()

            if (
                "how are you" in previous_bot_message
                or "how are you feeling" in previous_bot_message
                or "how are you doing" in previous_bot_message
            ):

                positive_responses = [
                    "good",
                    "im good",
                    "i'm good",
                    "i am good",
                    "fine",
                    "im fine",
                    "i'm fine",
                    "i am fine",
                    "great",
                    "im great",
                    "i'm great",
                    "i am great",
                    "doing good",
                    "doing great",
                    "feeling good",
                    "feeling great",
                    "pretty good",
                    "okay",
                    "ok",
                ]

                negative_responses = [
                    "sad",
                    "im sad",
                    "i'm sad",
                    "i am sad",
                    "bad",
                    "not good",
                    "im not good",
                    "i'm not good",
                    "i am not good",
                    "not well",
                    "im not well",
                    "i'm not well",
                    "i am not well",
                    "feeling bad",
                    "feeling sad",
                ]

                if message in positive_responses:

                    result = {
                        "intent": "conversation_positive",
                        "probability": "1.0",
                        "response": (
                            "That's great to hear! 😊 "
                            "What can I help you with today?"
                        ),
                    }

                elif message in negative_responses:

                    result = {
                        "intent": "conversation_negative",
                        "probability": "1.0",
                        "response": (
                            "I'm sorry to hear that. 💙 "
                            "Is there anything I can help you with?"
                        ),
                    }

        # ==================================================
        # 4. NORMAL NLP MODEL
        # ==================================================

        if result is None:
            result = self.predictor.predict(user_message)

        # ==================================================
        # 5. SAVE CONVERSATION
        # ==================================================

        save_chat(
            db=db,
            user_message=user_message,
            bot_response=result["response"],
            intent=result["intent"],
        )

        return result