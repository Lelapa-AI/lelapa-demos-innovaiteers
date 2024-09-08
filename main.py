import google.generativeai as genai
from flask import Flask, request, session
from flask_session import Session
from google.api_core.exceptions import ResourceExhausted
from translator import data
from handle_media import determine_media
from message_handler import send_message
from vuvusetup import translator, LANGUAGES
import profiling_handler

# Init the Flask App
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

language = ""
app.secret_key = "bunda"

genai.configure(api_key='AIzaSyDRF5ylqwU_zjA1eymJQn1EybLdbxuxePc')

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="This system should be \ndesigned to assist users in obtaining  insurance quotations such as vehicle,home,life,health.for vehicle It will ask for necessary details such as vehicle information, driving history, and coverage preferences. It will provide users with estimated quotes based on the input provided. It aims to be helpful, clear, and efficient, ensuring users receive accurate and timely information. The bot should avoid asking too many questions at once, and instead, ask prompt by prompt, keeping the questions simple. Maintain a cheerful and professional tone, using simple language. Even if the user is negative, keep a positive and helpful attitude. Keep the conversation focused on providing the insurance quote and avoid straying away from the topic. The bot will use calculations and vehicle data to provide accurate quotes based on the information given by the user, with all calculations done in South African Rands (ZAR) the bot should give a rough estimate. Always ask one question at a time when requesting information from the user. For example, when asking for the make, model, and year of a car, the bot will break it down into separate questions: 'What is the make of your car?', 'What is the model of your car?', and 'What is the year of your car?'. The bot can also switch languages anytime during the conversation if the user requests it because different languages can be used leveraging other apis to understand the user the system can continue responding in english it will get translated by another api do not mention that you are still prompting in english.do not try translate the language continue prompting the same prompt after a language change request. If asked questions not related to car insurance or the scope of the bot, the bot will respectfully decline to answer and gently steer the conversation back to car insurance.Take into account of where the vehicle parks in a safe home garage, complex parking or street.Ignore the words such as 'zulu','isizulu','isixhosa','xhosa','tsonga'.the system is not alone most capabilities it cannot peform have been outsourced it should proceed as if it knows how to do everything.The system should allow users to send images of their vehicle if they want to  and use it to make out the make and understand it will be getting text as another api will be getting the model using the image. The model should not prompt user for vehicle image it should wait for the user to offer the vehicle picture",
)


# chat_session = model.start_chat(
#   history=[]
# )

def ai_prompt(prompt, his):
    try:
        # print(prompt)
        print(his)
        chat_session = model.start_chat(
            history=his
        )
        response = chat_session.send_message(prompt)
        # print(response.text)
        return response.text
    except ResourceExhausted:
        return "I do not understand that at the moment please try again in a Few minutes."

users = []

#  chats are [{user_id: [dict{}]}]
chats = []
@app.route('/audio', methods=['POST', 'GET'])
def audio_handler():
    print("I've received some audio")



def find_chat(user_id):
    for i in chats:
        if user_id in i.keys():
            return i[user_id]



@app.route('/chatbot', methods=['POST'])
def chatgpt():
    try:
        type, message, user_id = determine_media(request)
        
        if message == "complete":
            profiling_handler.write_file_to_pdf(user_id)

        # print(message)
        if type == "audio":
            return send_message("")

        if user_id not in users:  # session coming from Flask
            users.append(user_id)
            chats.append({user_id: []})


        # Add user input to the session
        message_lang = message.lower().split()
        for i in message_lang:
            if i in LANGUAGES.keys():
                global data
                data['language'] = i
                # print(data)
                break
        # session['history'].append({"role": "user", "parts": [message]})
        user_history = find_chat(user_id)
        user_history.append({"role": "user", "parts": [message]})
        profiling_handler.write_to_text("user",message,user_id)

        # convert the message to english so ai can understand
        ai_response = ai_prompt(translator(message, data['language'], "english"),user_history)

        # session['history'].append({"role": "model", "parts": [ai_response]})
        user_history.append({"role": "model", "parts": [ai_response]})
        profiling_handler.write_to_text("model",ai_response,"AI Bot")



        if data['language'] != "english":
            ai_response = translator(ai_response, "english", data['language'])
        return send_message(ai_response)


    except Exception as e:
        print(f"An exception occured in main.py {e}")
        return "An error occured", 500


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
