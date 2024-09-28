import requests
import base64

# Define the URL of your Worker
url = 'https://snapsight2.jacomoolman1890.workers.dev/'

# Specify the path to your image file
# image_path = 'dog.jpg'
image_path = 'sun.jpg'

# Read the image file and encode it as base64
with open(image_path, 'rb') as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

# Prepare the JSON payload
payload = {
    'image': image_base64,
    'prompt': 'What time of day is this?'
}

# Send the POST request
headers = {
    'Content-Type': 'application/json'
}
response = requests.post(url, headers=headers, json=payload)

# Print the response from the Worker
print(response.status_code)
print(response.text)
