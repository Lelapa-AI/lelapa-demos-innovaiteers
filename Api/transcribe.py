from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account

client_file = "qoutelynx-afeb607d0f34.json"
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials=credentials)

first_lang = "en-US"
second_lang = "es"

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


if __name__ == "__main__":
    print(speech_recognition("audios.wav"))