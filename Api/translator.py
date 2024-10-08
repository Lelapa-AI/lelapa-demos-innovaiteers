from Api.vuvusetup import object_recognise,translator,LANGUAGES,speech_to_text

import os


data  = {
    "model" : "",
    "make"  : "",
    "year"  : 0,
    "language": "english",
 }


def extract_data(data_):
    for i in data_:
        if i["entity"].lower() == "organisation":
            data["make"] = i["word"]
        if i["entity"].lower() == "date":
            data["year"] = i["word"]
        if i["entity"].lower() == "model":
            data["model"] = i["word"]



def language_detector(sentence):
    for lang in LANGUAGES:
        sentence_ = translator(sentence,lang,lang)
        if sentence == sentence_:
            return True


def speech_text(content="audios.wav"):
    if content != "audios.wav":
        return
    FILE_SIZE = os.path.getsize(content)
    speech_to_text(content,FILE_SIZE)

    

def get_data(sentence,prod=False):
    if not prod:
        return
    json  = object_recognise(sentence.lower())
    if json == []:
        return
    extract_data(json)
    json = object_recognise(sentence.upper())
    if json == []:
        return
    extract_data(json)
    if "" not in [data['make'], data['year'], data["model"]]:
        return data
    if "" in data["model"]:
        return "model"
    if "" in data['make']:
        return "make"
    if 0 == data["year"]:
        return "year"
    return

