from retry import retry
from requests import Session,post
import base64
from os import getenv
from dotenv import load_dotenv
load_dotenv()



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

headers={"X-CLIENT-TOKEN": VULAVULA_TOKEN,}
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
    print(response.json())
    # return sentence if failed to translate
    if response.status_code != 200:
        return sentence
    return response.json()["translation"][0]["translation_text"]



def object_recognise(sentence):
    session = retry(Session(), tries=10, backoff=1)

    ner = post(
    NER_URL,
    json={"encoded_text": sentence},
    headers=headers,)
    data = ner.json()
    new_data = []
    for data_ in data:
        new__data = {
            "entity": data_["entity"],
            "word": data_["word"]
        }
        new_data.append(new__data)
    return new_data



def speech_to_text(content,file_size):
    # Open file in binary mode
    with open(content, 'rb') as file:
        # Read file
        file_content = file.read()

    # Encode file content
    encoded_content = base64.b64encode(file_content)

    # Decode bytes to string
    encoded_string = encoded_content.decode()

    transport_request_body = {
        "file_name": content,
        "audio_blob": encoded_string,
        "file_size": file_size,
    }

    headers={
        "X-CLIENT-TOKEN": VULAVULA_TOKEN,
    }

    resp = post(
        "https://vulavula-services.lelapa.ai/api/v1/transport/file-upload",
        json=transport_request_body,
        headers=headers,
    )

    upload_id = resp.json()["upload_id"]

    headers={
        "X-CLIENT-TOKEN": VULAVULA_TOKEN,
    }

    process = post(
        f"https://vulavula-services.lelapa.ai/api/v1/transcribe/process/{upload_id}",
        json={
            # "webhook": <INSERT_URL>,
            "language_code":"zul"
        },
        headers=headers,
    )
    x = 0
    while process.json()["status"] == 'Message sent to process queue.':
        x += 1 
        print(x)
        if x == 100:
            return "failed"
        
    print(process.json())
    return resp.json()

