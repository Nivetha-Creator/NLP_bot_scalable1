import pickle
from pathlib import Path

from tensorflow.keras.models import load_model


BASE_DIR = Path(__file__).resolve().parents[3]
MODELS_DIR = BASE_DIR / "models"

MODEL_FILE = MODELS_DIR / "chatbot_model.h5"
WORDS_FILE = MODELS_DIR / "words.pkl"
CLASSES_FILE = MODELS_DIR / "classes.pkl"


def load_chatbot():
    model = load_model(MODEL_FILE)

    with open(WORDS_FILE, "rb") as file:
        words = pickle.load(file)

    with open(CLASSES_FILE, "rb") as file:
        classes = pickle.load(file)

    return model, words, classes