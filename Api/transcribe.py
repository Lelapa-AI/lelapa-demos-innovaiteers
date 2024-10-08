from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
from requests import post
import base64
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
VULAVULA_TOKEN = os.getenv("VULAVULA_KEY")
VULAVULA_TRANSCRIBE_URL = "https://vulavula-services.lelapa.ai//api/v1/transcribe/sync"
client_file = "qoutelynx-afeb607d0f34.json"
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials=credentials)

first_lang = "en-US"
second_lang = "es"


def speech_text(content="audios.wav"):
    """Transcribes audio using Lelapi first if fails uses ai
    Args:
        content (str, optional): _description_. Defaults to "audios.wav".
    Returns:
        String: Returns transcribed audio either from lepai or ai
    """
    FILE_SIZE = os.path.getsize(content)
    possible_trascption = speech_to_text_vula(content,FILE_SIZE)
    if possible_trascption == {'Lelapi':"offline"}: 
        return speech_recognition(content)
    else:
        return possible_trascption


def speech_recognition(speech_file):
    try:
        with open(speech_file, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            audio_channel_count=2,
            language_code=first_lang,
            alternative_language_codes=['st-ZA','zu-ZA','xh-ZA','en-ZA','tn-ZA','nso-ZA','ss-ZA','af-ZA','sw-ZA']
        )

        print("Waiting for operation to complete...")
        response = client.recognize(config=config, audio=audio)
        print(response.results)

        for i, result in enumerate(response.results):
            alternative = result.alternatives[0]
            print("-" * 20)
            print(f"First alternative of result {i}: {alternative}")
            print(f"Transcript: {alternative.transcript}")

        return response.results[0].alternatives[0].transcript
    
    except IndexError:
        return "Error while listening to voice note ask for a clear voice note or suggest typing"


def speech_to_text_vula(content,file_size):
    """Lelapi_transcrption

    Args:
        content (_type_): _description_
        file_size (_type_): _description_
    """

    # Open file in binary mode
    with open(content, 'rb') as file:
        # Read file
        file_content = file.read()

    # Encode file content
    encoded_content = base64.b64encode(file_content)

    # Decode bytes to string
    encoded_string = encoded_content.decode()
    
    # The req can also take the preffered language
    transport_request_body = {
        "file_name": content,
        "audio_blob": encoded_string,
        # 'language_code': 'eng',
        "file_size": 0,
    }

    headers1 = {
    'Content-Type': 'application/json',
    'X-CLIENT-TOKEN': VULAVULA_TOKEN
    }


    resp = post(
        VULAVULA_TRANSCRIBE_URL,
        json=transport_request_body,
        headers=headers1,
    )
   

    try: 
        response_transcribe = resp.json()
        
        # Access the 'text' key and check its length
        text = response_transcribe.get('text', "")  # Safely get the 'text' key or default to empty string
        if len(text) > 3:
            return text
        else:
            return "User voice note not clear"
    except:
        return {'Lelapi':"offline"}



if __name__ == "__main__":
    print(speech_text("about_time.wav"))