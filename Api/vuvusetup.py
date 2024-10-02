# from retry import retry
from requests import Session,post
import base64
from os import getenv
from dotenv import load_dotenv
import os
import assemblyai as aai
from time import sleep
load_dotenv()


VULAVULA_TRANSCRIBE_URL = "https://vulavula-services.lelapa.ai//api/v1/transcribe/sync"
VULAVULA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImZmYjk4MzIwNDE3ZTRhODBhMDQ2YmExZDNlZmJhNTM4IiwiY2xpZW50X2lkIjoxNSwicmVxdWVzdHNfcGVyX21pbnV0ZSI6MCwibGFzdF9yZXF1ZXN0X3RpbWUiOm51bGx9.QMnha4-WdPPV0kqclkCgjg7Q5iRMiiFyUqhMBDDwJ7o"
VULAVULA_BASE_URL = 'https://vulavula-services.lelapa.ai/api/v1/'
LANGUAGES = {
        "sotho": "nso_Latn",
        "afrikaans": "afr_Latn",
        "southern sotho": "sot_Latn",
        "swati": "ssw_Latn",
        "tsonga": "tso_Latn",
        "tswana": "tsn_Latn",
        "xhosa": "xho_Latn",
        "zulu": "zul_Latn",
        "english": "eng_Latn",
        "swahili": "swh_Latn"
    }

headers={"X-CLIENT-TOKEN": getenv("VULAVULA_KEY")}
aai.settings.api_key = getenv("ASSAMBLYAI")
# The transport API to upload your file
TRANSPORT_URL = VULAVULA_BASE_URL+"transport/file-upload"
 
# The transcribe API URL to kick off your transcription job.
TRANSCRIBE_URL = VULAVULA_BASE_URL + "transcribe/process/"
NER_URL = VULAVULA_BASE_URL + 'entity_recognition/process'
TRANSLATE_URL = VULAVULA_BASE_URL + "translate/process"
# When transcription is complete, our system calls a webhook that you provide.
# Here, we’re using a demo webhook from webhook.site for testing.
WEBHOOK_URL="https://webhook.site/3594b17d-a879-41b8-bb28-e59d08e16be6"
 
# Name of the file you are transcribing
FILE_TO_TRANSCRIBE = "<FILE TO TRANSCRIBE>"



def translator(sentence,lang,target):


    data = {
            "input_text": sentence,
            "source_lang": LANGUAGES.get(lang),
            "target_lang": LANGUAGES.get(target)
    }
    # Sending POST request
    response =  post(TRANSLATE_URL, headers=headers, json=data)
    # return sentence if failed to translate
    if response.status_code != 200:
        return sentence
    return response.json()["translation"][0]["translated_text"]



# def object_recognise(sentence):
#     session = retry(Session(), tries=10, backoff=1)

#     ner = post(
#     NER_URL,
#     json={"encoded_text": sentence},
#     headers=headers,)
#     data = ner.json()
#     new_data = []
#     for data_ in data:
#         new__data = {
#             "entity": data_["entity"],
#             "word": data_["word"]
#         }
#         new_data.append(new__data)
#     return new_data

"""Works now"""
def speech_to_text_AI(audiopath):
    # Initialize the Transcriber object
    transcriber = aai.Transcriber()

    # Transcribe the audio from the provided path
    transcript = transcriber.transcribe(audiopath)

    # Check the status of the transcript
    if transcript.status == aai.TranscriptStatus.error:
        # If there's an error, print the error message
        print(f"Transcription failed: {transcript.error}")
        return None  # Return None to indicate failure
    elif transcript.status == aai.TranscriptStatus.completed:
        # If transcription is successful, print and return the transcript text
        print(transcript.text)
        return transcript.text
    else:
        # Handle other statuses like 'processing' or 'queued'
        print(f"Transcript is currently {transcript.status}.")
        return None  # Return None as the process is not complete


def speech_to_text(content,file_size):
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
    'X-CLIENT-TOKEN': getenv("VULAVULA_KEY")
    }


    resp = post(
        VULAVULA_TRANSCRIBE_URL,
        json=transport_request_body,
        headers=headers1,
    )

    try:
        return resp.json()['text']
    except:
        return {'Lelapi':"offline"}

    
    

def speech_text(content="audios.wav"):
    """Transcribes audio using Lelapi first if fails uses ai

    Args:
        content (str, optional): _description_. Defaults to "audios.wav".

    Returns:
        String: Returns transcribed audio either from lepai or ai
    """
    if content != "audios.wav":
        return
    FILE_SIZE = os.path.getsize(content)
    possible_trascption = speech_to_text(content,FILE_SIZE)
    if possible_trascption == {'Lelapi':"offline"}: 
        return speech_to_text_AI(content)
    else:
        return possible_trascption
        
# print(speech_text("audios.wav")) Test
