import os
import requests
from translator import speech_text
from requests.auth import HTTPBasicAuth

from dotenv import load_dotenv
load_dotenv()
import car_detector

import google.generativeai as genai




def handle_media(request, msg):
    """Function to handle incoming media."""
    media_url = request.values.get('MediaUrl0', '')  # URL of the attached media
    media_type = request.values.get('MediaContentType0', '')
    
    if media_type.startswith('image/'):
        msg.body("Thank you for sending an image.")
        print(f"Received an image: {media_url}")
    elif media_type == 'audio/ogg' or media_type.startswith('audio/ogg'):
        msg.body("Thank you for sending a voice note.")
        print(f"Received a voice note: {media_url}")
        # Here, you can add code to handle the voice note, like transcribing it
    else:
        msg.body("Received file is neither an image nor a voice note.")
        print(f"Received other type of file: {media_type}")


def download_audio(response):
    try:
        # response = requests.get(media_url)
        with open('audios.wav', 'wb') as f:
            print("I a printing in audio down")
            f.write(response)
            return True
    except requests.RequestException as e:
        print(f"Failed to download the file: {e}")


def format_response(data):
    try:
        if len([data]) == 1:
            car_data = f"Make: {data['make_name']}, Model: {data['model_name']}, Years: {data['years']}"
            return car_data.lower()
        return data
    except:
        return "car not found"
        




def determine_media(request):

    num_media = int(request.values.get('NumMedia', 0)) 
    if num_media > 0:
        media_type = request.values.get('MediaContentType0', '')
        media_url = request.values.get('MediaUrl0', '')
        response = requests.get(media_url, auth=HTTPBasicAuth(os.getenv("TWILLIO_SID"), os.getenv('TWILLIO_TOKEN')))

        if 'image' in media_type:

            response = car_detector.detect_car_details(response.content)
            car_data = format_response(response)
            return "car", car_data, request.values.get("WaId","")

        elif 'audio' in media_type:
            # Issue with handling audio
            download_audio(response.content)
            return "audio" , speech_text(), request.values.get("WaId","")

    else:
        return "text",request.values.get('Body', '').lower(), request.values.get("WaId","")
    






def process_images(image_file):
  genai.configure(api_key=os.getenv("GEMINI_CHAT_API"))

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
Analyze the image thoroughly and determine the details of the car in the image.
Extract the make, model and the manufacture year.
Only base your answers strictly on what information is available in the image attached.
Do not make up any information that is not part of the image and do not be too
verbose, be to the point.
If the image is not that of a car, politely point out that no car was detected in the image.

Questions to be answered based on the details of the car in the image:
- What make is the car.
- What model is the car.
- When year was the car released.
# """
    
    # "This system should be designed to assist users with accounting tasks, including generating detailed JSON responses for invoices, tracking expenses, revenue, and profits, and asking for daily expenses. The bot should follow these specific instructions:\n\n1. **Generate Invoices (JSON Response):**\n   - Return a JSON response with the following structure:\n     ```json\n     {\n       \"products\": [\n         {\n           \"description\": \"Product Description\",\n           \"quantity\": 0,\n           \"unit_price\": 0.0,\n           \"total\": 0.0\n         }\n       ],\n       \"subtotal\": 0.0,\n       \"markup\": 0.0,\n       \"total\": 0.0,\n       \"dollar_equivalent\": 0.0,\n       \"rate_used\": 0.0\n     }\n     ```\n   - Calculate markup at the end of the invoice:\n     - Standard items: 30% markup.\n     - Large items (fridges, TVs, furniture, washing machines, dishwashing machines): 40% markup.\n     - The model should assess if an item is standard or large and apply the appropriate markup.\n   - Ensure the JSON response is generated chronologically.\n   - Use a unique numbering system for the JSON responses.\n\n2. **Track Expenses:**\n   - Maintain a record of daily expenses.\n   - Ask users for daily expense details.\n\n3. **Track Revenue:**\n   - Record and track revenue from generated JSON responses.\n\n4. **Track Profits:**\n   - Calculate net profit based on recorded expenses and revenue.\n\nThe bot aims to be helpful, clear, and efficient, ensuring users receive accurate and timely information. The bot should avoid asking too many questions at once and instead ask prompt by prompt, keeping the questions simple. Maintain a cheerful and professional tone, using simple language. Even if the user is negative, keep a positive and helpful attitude.\n\nThe bot will use calculations to provide accurate financial records based on the information given by the user. Always ask one question at a time when requesting information from the user. For example, when asking for daily expenses, the bot will break it down into separate questions: \"What was your expense for today?\", \"Could you provide the amount?\", and \"What was the nature of this expense?\".\n\nIf asked questions not related to accounting or the scope of the bot, the bot will respectfully decline to answer and gently steer the conversation back to accounting tasks. The system should allow users to send images of receipts if they want to and use it to track expenses, but the model should not prompt the user for receipt images; it should wait for the user to offer them.\n\nThe system should confirm the final rate used to calculate the dollar equivalent in the JSON response. Remember to maintain a polite, professional, and helpful demeanor throughout the interaction.",
  )

    # Upload the file and print a confirmation.
  sample_file = genai.upload_file(path=image_file,
                              display_name="Sample image 1")

  print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

  file = genai.get_file(name=sample_file.name)
  print(f"Retrieved file '{file.display_name}' as: {sample_file.uri}")

   # Create the prompt.
  prompt = "Describe the contents of the image and ascertain the contents that should be in the invoice based on the images"

  # Make the LLM request.
  print("Making LLM inference request...")
  response = model.generate_content([sample_file, prompt],
  request_options={"timeout": 600})
  print(response.text)





