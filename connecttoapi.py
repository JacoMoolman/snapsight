import requests

# Define the URL of your Worker
url = 'https://snapsight2.jacomoolman1890.workers.dev/'

# Specify the path to your image file
# image_path = 'sun.jpg'
image_path = 'dog.jpg'

# Open the image file in binary mode and send the POST request
with open(image_path, 'rb') as image_file:
    headers = {
        'Content-Type': 'image/jpeg'  # Adjust the content type based on the image format (e.g., image/png)
    }
    response = requests.post(url, headers=headers, data=image_file)

# Print the response from the Worker
print(response.status_code)
print(response.text)
