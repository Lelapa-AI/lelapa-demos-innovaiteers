import google.generativeai as genai
from flask import Flask, request, session
from handle_media import determine_media
import message_handler
from twilio.twiml.messaging_response import MessagingResponse
import os
from google.api_core.exceptions import ResourceExhausted
from vuvusetup import translator, LANGUAGES
from translator import data, get_data
# Init the Flask App
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management
language = ""
# Install the Google AI Python SDK: pip install google-generativeai
genai.configure(api_key='AIzaSyBG3Jc-pGQxTISOFWwZiEgPhbQoAPEEe7Q')
# Create the model
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
def prompt_ai(prompt, sess):
    chat_session = model.start_chat(history=sess['history'])
    response = chat_session.send_message(prompt)
    return response.text
users = []
sess = []
@app.route('/chatbot', methods=['POST'])
def chatgpt():
    try:
        # Determine the type of message, message content, and user phone number
        type, message, user_id = determine_media(request)
        # Check if the user is new or returning
        if user_id not in users:
            users.append(user_id)
            sess.append({"user_id": user_id, "history":[]})
            for i in sess:
                if i["user_id"] == user_id:
                    i["history"].append({"role": "user", "parts": [message]})
                    res= prompt_ai(message, i)
                    i['history'].append({
        "role": "model",
        "parts": [res],
    })
                    response = message_handler.send_message(res, user_id)
                    print(i)
                    return response
        else:
            for i in sess:
                if i["user_id"] == user_id:
                    i["history"].append({"role": "user", "parts": [message]})
                    res = prompt_ai(message, i)
                    i['history'].append({
        "role": "model",
        "parts": [res],
    })
                    response = message_handler.send_message(res, user_id)
                    return response
        # If the user is new or returning, but no response was generated
        return "No valid response generated", 200
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred", 500
# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)