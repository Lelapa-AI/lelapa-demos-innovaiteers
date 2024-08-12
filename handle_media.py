import os
import requests
from car_detector import detect_car_details
from translator import speech_text
from requests.auth import HTTPBasicAuth


voice_note_count = 0
voice_notes = {
    1: "said 1",
}


def handle_media(request, msg):
    """Function to handle incoming media."""
    media_url = request.values.get("MediaUrl0", "")  # URL of the attached media
    media_type = request.values.get("MediaContentType0", "")

    if media_type.startswith("image/"):
        msg.body("Thank you for sending an image.")
        print(f"Received an image: {media_url}")
    elif media_type == "audio/ogg" or media_type.startswith("audio/ogg"):
        msg.body("Thank you for sending a voice note.")
        print(f"Received a voice note: {media_url}")
        # Here, you can add code to handle the voice note, like transcribing it
    else:
        msg.body("Received file is neither an image nor a voice note.")
        print(f"Received other type of file: {media_type}")


def download_audio(response):
    try:
        # response = requests.get(media_url)
        with open("audios.wav", "wb") as f:
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

    num_media = int(request.values.get("NumMedia", 0))
    if num_media > 0:
        media_type = request.values.get("MediaContentType0", "")
        media_url = request.values.get("MediaUrl0", "")
        response = requests.get(
            media_url,
            auth=HTTPBasicAuth(
                "AC38ac74d05b32396fae97f3bd05cc3213", "287e77d92e74784ebf8f1ceb6d7fc9c0"
            ),
        )

        if "image" in media_type:

            response = detect_car_details(response)
            car_data = format_response(response)

        elif "audio" in media_type:
            global voice_note_count
            if voice_note_count < 1:
                voice_note_count += 1
                return voice_notes.get(voice_note_count)

            elif download_audio(response.content):
                return speech_text()

        return car_data

    else:
        return request.values.get("Body", "").lower()
