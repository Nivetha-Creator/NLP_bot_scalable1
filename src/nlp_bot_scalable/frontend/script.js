const API_URL = "https://nlp-bot-scalable1-b.onrender.com";

const input = document.getElementById("message");
const chatBox = document.getElementById("chat-box");
const sendButton = document.getElementById("send-button");
const newChatButton = document.getElementById("new-chat");


/* =========================
   ADD MESSAGE
========================= */

function addMessage(sender, message) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add(
        "message",
        sender === "user"
            ? "user-message"
            : "bot-message"
    );

    const avatar = document.createElement("div");

    avatar.classList.add("avatar");

    avatar.textContent =
        sender === "user" ? "👤" : "🤖";


    const content = document.createElement("div");

    content.classList.add("message-content");


    const senderName = document.createElement("span");

    senderName.classList.add("sender");

    senderName.textContent =
        sender === "user" ? "You" : "Bot";


    const bubble = document.createElement("div");

    bubble.classList.add("bubble");

    bubble.textContent = message;


    content.appendChild(senderName);
    content.appendChild(bubble);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);

    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}


/* =========================
   TYPING INDICATOR
========================= */

function showTyping() {

    const typing = document.createElement("div");

    typing.id = "typing";

    typing.classList.add(
        "message",
        "bot-message"
    );

    typing.innerHTML = `
        <div class="avatar">🤖</div>

        <div class="message-content">
            <span class="sender">Bot</span>

            <div class="bubble">
                Typing...
            </div>
        </div>
    `;

    chatBox.appendChild(typing);

    chatBox.scrollTop = chatBox.scrollHeight;
}


function removeTyping() {

    const typing =
        document.getElementById("typing");

    if (typing) {
        typing.remove();
    }
}


/* =========================
   SEND MESSAGE
========================= */

async function sendMessage() {

    const message = input.value.trim();

    if (!message) {
        return;
    }


    addMessage("user", message);

    input.value = "";

    sendButton.disabled = true;

    showTyping();


    try {

        const response = await fetch(
            `${API_URL}/chat`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message
                })
            }
        );


        if (!response.ok) {
            throw new Error("Server error");
        }


        const data = await response.json();

        removeTyping();


        addMessage(
            "bot",
            data.response
        );


    } catch (error) {

        removeTyping();

        addMessage(
            "bot",
            "Sorry, I couldn't connect to the chatbot server."
        );

        console.error(error);

    } finally {

        sendButton.disabled = false;

        input.focus();
    }
}


/* =========================
   ENTER KEY
========================= */

input.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }

    }
);


/* =========================
   LOAD PREVIOUS CHATS
========================= */

async function loadHistory() {

    try {

        const response = await fetch(
            `${API_URL}/chat/history`
        );


        if (!response.ok) {
            return;
        }


        const history = await response.json();


        /*
         * History is returned newest-first,
         * so reverse it for normal conversation order.
         */

        history.reverse();

        chatBox.innerHTML = "";


        history.forEach(chat => {

            addMessage(
                "user",
                chat.user_message
            );

            addMessage(
                "bot",
                chat.bot_response
            );

        });


    } catch (error) {

        console.log(
            "Could not load chat history."
        );

    }
}


/* =========================
   NEW CHAT
========================= */

if (newChatButton) {

    newChatButton.addEventListener(
        "click",
        function () {

            // Clear messages from the screen
            chatBox.innerHTML = "";

            // Clear input
            input.value = "";

            // Show fresh welcome message
            addMessage(
                "bot",
                "Hi! 👋 I'm your NLP assistant. How can I help you today?"
            );

            // Focus input
            input.focus();
        }
    );

}


/* =========================
   START CHATBOT
========================= */

loadHistory();
