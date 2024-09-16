from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from handle_media import determine_media,detect_language,translate_to_english
from play import connect_with_agent
from vuvusetup import translator
import google.generativeai as genai
import os



app = Flask(__name__)

os.environ['TWILIO_SID'] = ''
os.environ['TWILIO_TOKEN'] = ''

# Load the system instructions from a file
def get_system_string():
    with open('sysinstructions.txt', 'r') as file:
        return file.read()
    
# Set up the API key
genai.configure(api_key='')

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
chat_session = model.start_chat(history=[],enable_automatic_function_calling=True)


# Language codes
LANGUAGES = {
        "nso": "nso_Latn",
        "afr": "afr_Latn",
        "st": "sot_Latn",
        "sw": "ssw_Latn",
        "ts": "tso_Latn",
        "tswana": "tsn_Latn",
        "xh": "xho_Latn",
        "zu": "zul_Latn",
        "en": "eng_Latn",
        "sw": "swh_Latn"
    }




# Get the response from the model
def get_response(input_text,):
    
    response = chat_session.send_message(input_text)
    print(response.text)
    return response.text

# Send the response to the user
def send_message(message):

    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    if message == "car not found":
       msg.body("Oops I dont recognise vehicle maybe I can detail the car for me and I'll try figure the car out for you?")
    msg.body(message)
    return str(bot_resp)


# Webhook for the bot
@app.route('/Bot', methods=['POST'])
def webhook():
    try:
        type, message, user_id = determine_media(request)
        try:
            language = LANGUAGES[detect_language(message)]
        except KeyError:
            language = LANGUAGES["zu"]
        except TypeError:
            language = LANGUAGES['en']

        print(f"language: {language}")
        if language != LANGUAGES['en']:
            message = translate_to_english(message)
        print(message)
        response = get_response(message)
        if language != LANGUAGES['en']:
            return send_message(translator(response,'english',language))
        return send_message(response)
    
    except:
        return send_message("hmmm🤔 I seem to be down at the moment please try again in a few minutes.")

    


# running the app
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False,port=5000)