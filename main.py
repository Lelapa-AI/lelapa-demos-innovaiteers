import google.generativeai as genai
from flask import Flask, request, session
from handle_media import determine_media
from google.api_core.exceptions import ResourceExhausted
from vuvusetup import translator,object_recognise,LANGUAGES
from translator import data,get_data
from message_handler import send_message
import os


# Init the Flask App
app = Flask(__name__)
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
  system_instruction="""
This system is designed to assist users in obtaining insurance quotations for a wide variety of items and scenarios, including but not limited to:

- Vehicle insurance (cars, motorcycles, boats, etc.)
- Home and property insurance
- Life insurance
- Health insurance
- Phone and electronic device insurance
- Furniture and valuable item insurance
- Pet insurance
- Travel insurance

The system will ask for necessary details relevant to the type of insurance being quoted. It will provide users with estimated quotes based on the input provided. The system aims to be helpful, clear, and efficient, ensuring users receive accurate and timely information.

Key guidelines:
1. Ask questions one at a time, keeping them simple and clear.
2. Maintain a cheerful and professional tone, using simple language.
3. Keep a positive and helpful attitude, even if the user is negative.
4. Focus on providing insurance quotes and avoid straying from the topic.
5. Use calculations and relevant data to provide accurate quotes based on the information given by the user.
6. All calculations should be done in South African Rands (ZAR) unless specified otherwise.
7. Provide rough estimates when exact figures are not available.
8. Be able to switch languages if requested by the user, continuing the conversation seamlessly.
9. If asked questions outside the scope of insurance, respectfully decline and steer the conversation back to insurance topics.
10. Consider relevant factors for each insurance type (e.g., parking location for vehicles, health history for life insurance, etc.)
11. Allow users to send images of items they want to insure, and use the provided information to inform the quote process.
12. Do not prompt users for images; wait for them to offer this information.

The system should proceed as if it can handle all capabilities, even if some functions are outsourced to other APIs or services. Always strive to provide the most accurate and helpful insurance quotation experience possible for the user, regardless of the item or scenario they wish to insure.
"""
)

# chat_session = model.start_chat(
#   history=[]
# )

def ai_prompt(prompt,his):
  try:
    print(prompt)
    chat_session = model.start_chat(
  history=his
)
    response = chat_session.send_message(prompt)
    print(response.text)
    return response.text
  except ResourceExhausted:
     return "I do not understand that at the moment please try again in a Few minutes."


@app.route('/chatbot', methods=['POST'])
def  chatgpt():
    try:
      type, message, user_id = determine_media(request)

      if type == "audio":
         return send_message("feature in progress.")



      if user_id not in session: #session coming from Flask
              session['user_id'] = user_id
              session['history'] = []

      # Add user input to the session
      message_lang = message.lower().split()
      for i in message_lang:
        if i in LANGUAGES.keys():
          global data
          data['language'] = i
          # print(data)
          break
          
         
      # convert the message to english so ai can understand
      ai_response = ai_prompt(translator(message,data['language'],"english"),session['history'])

      session['history'].append({"role": "user", "parts": [message]})
      session['history'].append({"role": "model", "parts": [ai_response]})

      if data['language'] != "english":
        ai_response = translator(ai_response,"english",data['language'])
      return send_message(ai_response)
    

    except Exception as e:
      print(f"An exception occured in main.py {e}")
      return "An error occured", 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)