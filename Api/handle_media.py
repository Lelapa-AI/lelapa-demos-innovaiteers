from os import getenv
import requests
from .translator import speech_text
from requests.auth import HTTPBasicAuth
from googletrans import Translator
from .transcribe import speech_recognition

from .car_detector import detect_car_details

import google.generativeai as genai
from .object_identifier import recognize_image 

from dotenv import load_dotenv
load_dotenv()



translator = Translator()


def download_audio(content):
    try:
        # Write the audio content (passed directly) to a file
        with open('audios.wav', 'wb') as f:
            print("Writing audio file...")
            f.write(content)  # Write the raw content
        
        print("Audio saved successfully.")
        return True

    except Exception as e:
        print(f"Failed to save the audio file: {e}")
        return False



def format_response(data):
    try:
        if len([data]) == 1:
            car_data = f"Make: {data['make_name']}, Model: {data['model_name']}, Years: {data['years']}"
            return car_data.lower()
        return data
    except:
        return "car not found through image"
        



def determine_media(request):

    num_media = int(request.values.get('NumMedia', 0)) 
    if num_media > 0:
        media_type = request.values.get('MediaContentType0', '')
        media_url = request.values.get('MediaUrl0', '')
        response = requests.get(media_url, auth=HTTPBasicAuth(getenv("TWILIO_SID"), getenv("TWILIO_TOKEN")))
        print(response.content)
    

        if 'image' in media_type:
            save_image_from_bytes(response.content, f'./Assets/{request.values.get("WaId","")}_image.png')
            type_of_image = recognize_image(f'./Assets/{request.values.get("WaId","")}_image.png')

            match type_of_image:

                case "Vehicle detected":

                    response = detect_car_details(response.content)
                    car_data = format_response(response)
                    return "image", car_data, request.values.get("WaId","")
                
                case "Phone detected":
                    return "image",get_item_from_image(f'./Assets/{request.values.get("WaId","")}_image.png'), request.values.get("WaId","")
                
                case "Person detected":
                    return "image", "person detected make joke like you cannot insure a person", request.values.get("WaId","")
                
                case _:
                    return "image", get_item_from_image(f'./Assets/{request.values.get("WaId","")}_image.png'), request.values.get("WaId","")

        elif 'audio' in media_type:
            # Issue with handling audio
            if download_audio(response.content):
                return "audio" , speech_recognition('audios.wav'), request.values.get("WaId","")
            else:
                return "error", "Failed to download audio", request.values.get("WaId","")
            
    else:   
            message = request.values.get('Body', '').lower()
            if message == "":
                message = request.json["postprocessed_text"]
                if len(message) == 0:
                    raise IndexError
                message = message[0]["text"]
            return "text",message, request.values.get("WaId","")
        


    

    
def get_item_from_image(image_file):
    genai.configure(api_key=getenv("GEMINI_API_KEY"))

    def upload_to_gemini(path):
        file = genai.upload_file(path)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file

    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Your sole task is to identify the brand and model of an item from an image, if available. If the item has no identifiable brand or model, determine what the item is. Simply provide the name; no explanations are needed. Do not waste time.",
    )

    # TODO Make these files available on the local file system
    # You may need to update the file paths

    chat_session = model.generate_content([upload_to_gemini(image_file)], request_options={"timeout": 600})
    print(chat_session.text)
    return chat_session.text


def save_image_from_bytes(image_bytes, file_path):
    from PIL import Image
    import io
    """
    Save an image from a byte array to a local file.

    Parameters:
    image_bytes (bytes): The byte array of the image.
    file_path (str): The path where the image will be saved, including the file name and extension.

    Returns:
    None
    """
    try:
        # Create a BytesIO object from the image bytes
        image_stream = io.BytesIO(image_bytes)
        
        # Open the image using PIL
        image = Image.open(image_stream)
        
        # Save the image to the specified file path
        image.save(file_path)
        print(f"Image saved successfully at {file_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")


def detect_language(string):
    return translator.detect(string).lang

def translate_to_english(string):
    return translator.translate(string, dest='en').text


# if __name__ == "__main__":
#     print(detect_language("iphone 12 mini."))