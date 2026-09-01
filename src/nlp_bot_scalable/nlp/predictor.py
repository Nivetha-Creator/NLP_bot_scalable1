import json
import random
from pathlib import Path

import numpy as np

from nlp_bot_scalable.nlp.model_loader import load_chatbot
from nlp_bot_scalable.nlp.preprocessing import bag_of_words


class ChatbotPredictor:

    def __init__(self):
        # Load trained model, words, and classes
        self.model, self.words, self.classes = load_chatbot()

        # Find the project root directory
        BASE_DIR = Path(__file__).resolve().parents[3]

        # Path to intents.json
        INTENTS_FILE = BASE_DIR / "intents.json"

        # Load intents
        with open(INTENTS_FILE, "r", encoding="utf-8") as file:
            self.intents = json.load(file)["intents"]

    def predict(self, sentence: str):

        # Convert sentence into bag of words
        bow = bag_of_words(sentence, self.words)

        # Predict intent
        results = self.model.predict(
            np.array([bow]),
            verbose=0
        )[0]

        ERROR_THRESHOLD = 0.25

        # Filter predictions above threshold
        filtered_results = [
            [i, probability]
            for i, probability in enumerate(results)
            if probability > ERROR_THRESHOLD
        ]

        # Sort by probability
        filtered_results.sort(
            key=lambda x: x[1],
            reverse=True
        )

        # No matching intent
        if not filtered_results:
            return {
                "intent": None,
                "probability": None,
                "response": "Sorry, I didn't understand that."
            }

        # Get best intent
        best_intent = self.classes[filtered_results[0][0]]
        best_probability = filtered_results[0][1]

        # Default response
        response = "Sorry, I didn't understand that."

        # Find response for the predicted intent
        for intent in self.intents:

            if intent["tag"] == best_intent:
                response = random.choice(intent["responses"])
                break

        return {
            "intent": best_intent,
            "probability": str(best_probability),
            "response": response
        }


if __name__ == "__main__":

    predictor = ChatbotPredictor()

    result = predictor.predict("Hello")

    print(result)