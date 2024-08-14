import os
import requests
from translator import speech_text
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
load_dotenv()
import car_detector



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
    





