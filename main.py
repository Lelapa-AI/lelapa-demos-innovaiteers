import requests
from i10data import data


def detect_car_details(image_byte):

    # API endpoint
    url = "https://api.carnet.ai/v2/mmg/detect"

    # Query parameters
    params = {
        "box_offset": 0,
        "box_min_width": 100,
        "box_min_height": 100,
        "box_min_ratio": 0.50,
        "box_max_ratio": 3.15,
        "box_select": "center",
        "region": "EU",
    }

    # Headers
    headers = {
        "accept": "application/json",
        "api-key": "bfcc5c7a-3980-4e16-a7a1-b0e49a6402a6",  # Replace with # with 6
        "Content-Type": "application/octet-stream",
    }

    # Read the image file in binary mode
    # with open(image_path, 'rb') as img_file:
    #     img_data = img_file.read()

    # Send the POST request
    response = requests.post(url, params=params, headers=headers, data=image_byte)

    # Check if the request was successful
    if response.status_code == 200:
        return refine_raw_data(response.json())  # Return the JSON response
    else:
        return response.status_code, response.text  # Return error status and message


def refine_raw_data(response):
    # Loop through each detection
    for detection in response["detections"]:
        # Check if 'mmg' key exists and is not empty
        if "mmg" in detection and detection["mmg"]:
            # Return the first mmg entry that contains both 'make_id' and 'make_name'
            for mmg in detection["mmg"]:
                if "make_id" in mmg and "make_name" in mmg:
                    return mmg
    return {"Car": "Unrecognizable"}  # Return None if no matching mmg found


# Extract the mmg information

# image_path = 'images/20240629_115344.jpg'  # Replace with the path to your image
# car_details = detect_car_details(image_path)
# print(car_details)
