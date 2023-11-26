import requests
import re
import urllib.request
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

cookies = {'sessionid': os.getenv('INSTA_SESSION')}
headers = {'User-Agent':'Instagram 76.0.0.15.395 Android (24/7.0; 640dpi; 1440x2560; samsung; SM-G930F; herolte; samsungexynos8890; en_US; 138226743)'}

#finding media?id= using link
def find_media_id(reel_link):
    reel_data = requests.get(reel_link)
    pattern = re.compile(r'media\?id=\d+')
    match = pattern.search(reel_data.text)
    media_id = match.group().split('=')[-1]
    return media_id

#finding video url with media id
def find_reel_downloadable_url(media_id_of_reel):
    reel_video_link = f"https://i.instagram.com/api/v1/media/{media_id_of_reel}/info/"
    #getting data
    reel_video_data = requests.get(reel_video_link,headers=headers,cookies=cookies)
    json_data_for_link = reel_video_data.json()
    end_url = json_data_for_link['items'][0]['video_versions'][0]['url']
    return end_url


import cv2
import numpy as np
import requests
import numpy as np
import urllib

def extract_scene(video_url, output_image_path='output.jpg', change_threshold=0.5):
    # Open the video stream
    cap = cv2.VideoCapture(video_url)

    # Read the first frame
    _, prev_frame = cap.read()

    # Loop through the video frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Calculate the absolute difference between frames
        diff = cv2.absdiff(prev_frame, frame)

        # Convert the difference to grayscale
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # Threshold the grayscale difference
        _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)

        # Calculate the percentage of changed pixels
        changed_pixels_percentage = np.sum(thresh == 255) / thresh.size

        # Check if the percentage of changed pixels is above the threshold
        if changed_pixels_percentage > change_threshold:
            # Scene change detected, save the frame as an image
            cv2.imwrite(output_image_path, frame)
            return 1  # Scene change detected

        # Update the previous frame
        prev_frame = frame

    # Release video capture
    cap.release()

    # No scene change detected
    return 0

from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

ADMIN = os.getenv("ADMIN")
TOKEN = os.getenv("API_TOKEN")

def send_image():
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    files = {'photo': open("output.jpg", 'rb')}
    params = {'chat_id': ADMIN}

    response = requests.post(url, params=params, files=files)
    return response.json()

def send_msg(msg):
    endpoint = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    chat_id = ADMIN
    parameters = {'chat_id':chat_id,'text':msg}
    requests.get(url = endpoint, params = parameters)