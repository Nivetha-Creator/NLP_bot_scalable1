import nltk
import numpy as np

from nltk.stem import WordNetLemmatizer


nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("wordnet")


lemmatizer = WordNetLemmatizer()


def clean_up_sentence(sentence: str) -> list[str]:
    sentence_words = nltk.word_tokenize(sentence)

    return [
        lemmatizer.lemmatize(word.lower())
        for word in sentence_words
    ]


def bag_of_words(sentence: str, words: list[str]) -> np.ndarray:
    sentence_words = clean_up_sentence(sentence)

    bag = [0] * len(words)

    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)
