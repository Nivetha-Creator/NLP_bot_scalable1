import requests


API_URL = "http://127.0.0.1:8000/chat"


def chat():
    print("NLP Chatbot")
    print("Type 'exit' to quit.")
    print("-" * 40)

    while True:
        message = input("You: ")

        if message.lower() == "exit":
            print("Bot: Goodbye!")
            break

        try:
            response = requests.post(
                API_URL,
                json={"message": message}
            )

            response.raise_for_status()

            data = response.json()

            print(f"Bot: {data['response']}")

        except requests.RequestException as error:
            print(f"Error connecting to chatbot: {error}")


if __name__ == "__main__":
    chat()