# """
# Install the Google AI Python SDK

# $ pip install google-generativeai

# See the getting started guide for more information:
# https://ai.google.dev/gemini-api/docs/get-started/python
# """

# import os

# import google.generativeai as genai

# genai.configure(api_key='AIzaSyCjEe1_7C_2ZhaZtyoIVMHMqOBAYmC2gnc')

# # Create the model
# # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
# generation_config = {
#   "temperature": 1,
#   "top_p": 0.95,
#   "top_k": 64,
#   "max_output_tokens": 8192,
#   "response_mime_type": "text/plain",
# }

# model = genai.GenerativeModel(
#   model_name="gemini-1.5-pro",
#   generation_config=generation_config,
#   # safety_settings = Adjust safety settings
#   # See https://ai.google.dev/gemini-api/docs/safety-settings
#   system_instruction="This system should be \ndesigned to assist users in obtaining vehicle insurance quotations. It will ask for necessary details such as vehicle information, driving history, and coverage preferences. It will provide users with estimated quotes based on the input provided. It aims to be helpful, clear, and efficient, ensuring users receive accurate and timely information. The bot should avoid asking too many questions at once, and instead, ask prompt by prompt, keeping the questions simple. Maintain a cheerful and professional tone, using simple language. Even if the user is negative, keep a positive and helpful attitude. Keep the conversation focused on providing the insurance quote and avoid straying away from the topic. The bot will use calculations and vehicle data to provide accurate quotes based on the information given by the user, with all calculations done in South African Rands (ZAR). Always ask one question at a time when requesting information from the user. For example, when asking for the make, model, and year of a car, the bot will break it down into separate questions: 'What is the make of your car?', 'What is the model of your car?', and 'What is the year of your car?'. The bot will support multiple languages, asking users for their language preference at the start and switching to their preferred language for the conversation. The bot can also switch languages anytime during the conversation if the user requests it. If asked questions not related to car insurance or the scope of the bot, the bot will respectfully decline to answer and gently steer the conversation back to car insurance.Take into account the address of where the vehicle parks.",
# )

# chat_session = model.start_chat(
#   history=[]
# )
# while True:
#     inp = input("prompt: ")
#     response = chat_session.send_message(inp)

#     print(response.text)


# from google.cloud import translate_v2 as translate

# client = translate.Client()

# text = "Hallo, wie geht's?"
# result = client.detect_language(text)
# print(result['language'])  # Output: 'de'
