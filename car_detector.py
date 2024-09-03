import requests
from ast import literal_eval

url = "http://localhost:7000/"

def detect_car_details(image_byte):
    response = requests.post(url,data=image_byte)
    if response.status_code == 200:
        # converting from byte to dict
        my_json = literal_eval(response.content.decode('utf8').replace("'", '"'))
        return my_json["description"]
    else:
        return {}
