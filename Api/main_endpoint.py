from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from .handle_media import determine_media, detect_language, translate_to_english
from .service import connect_with_agent
from .vuvusetup import translator
import google.generativeai as genai
from dotenv import load_dotenv
from os import getenv
import logging

load_dotenv()
app = Flask(__name__)
app.secret_key = "bunda"


# Load the system instructions from a file
def get_system_string():
    with open("sysinstructions.txt", "r") as file:
        return file.read()


# Set up the API key
genai.configure(api_key=getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# set up the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=get_system_string(),
    tools=[connect_with_agent],
)
# Start a chat session
chat_session = model.start_chat(history=[], enable_automatic_function_calling=True)


# Language codes
LANGUAGES = {
    "nso": "nso_Latn",
    "afr": "afr_Latn",
    "af": "afr_Latn",
    "st": "sot_Latn",
    "sw": "ssw_Latn",
    "ts": "tso_Latn",
    "tswana": "tsn_Latn",
    "xh": "xho_Latn",
    "zu": "zul_Latn",
    "en": "eng_Latn",
    "sw": "swh_Latn",
}


# Get the response from the model
def get_response(input_text, history):
    chat_session = model.start_chat(
        history=history, enable_automatic_function_calling=True
    )
    response = chat_session.send_message(input_text)
    print(response.text)
    return response.text


# Send the response to the user
def send_message(message):

    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    if message == "car not found":
        msg.body(
            "Oops I dont recognise the vehicle maybe you can get the car details for me and I'll try figure the car out for you?"
        )
    msg.body(message)
    return str(bot_resp)


users = []
chats = {}

logging.basicConfig(level=logging.INFO)


# Testing endpoint
@app.route("/", methods=["GET"])
def test_endpoint():
    return "API is deployed correctly and functional!"


# Webhook for the bot
@app.route("/Bot", methods=["POST"])
def webhook():

    # try:
    type, message, user_id = determine_media(request)

    if user_id not in users:
        users.append(user_id)
        chats[user_id] = []
    print(chats)
    print(users)
    try:
        code = detect_language(message)
        print(code)
        language = LANGUAGES[code]
    except KeyError:
        language = LANGUAGES["zu"]
    except TypeError:
        language = LANGUAGES["en"]

    print(f"language: {language}")

    if language != LANGUAGES["en"]:
        message = translate_to_english(message)

    print(message)
    response = get_response(message, chats[user_id])
    chats[user_id].append({"role": "user", "parts": [message]})
    chats[user_id].append({"role": "model", "parts": [response]})

    if language != LANGUAGES["en"]:
        return send_message(translator(response, "english", language))
    return send_message(response)


# except Exception as e:
#     logging.error(f"Error occured: {str(e)}")
# return send_message(
#     "hmmm🤔 I seem to be down at the moment please try again in a few minutes."
# )


# running the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5000)
