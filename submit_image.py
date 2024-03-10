import requests
from PIL import Image
import io
import os

try:
    from PIL import ImageResampling
except ImportError:
    ImageResampling = Image

# URL of the Flask API endpoint for file uploads
url = '192.168.3.28'

# Path to the image file you want to upload
# file_path = 'E:\\print\\20230610_085734.jpg'
# file_path = 'E:\\print\\JacoPuzzle1-ORI.jpg' #Puzzle
# file_path = 'E:\\print\\DSC00704.jpg' #Fisherman
file_path = 'E:\\print\\IMG-20230617-WA0059.jpg' #Jm red shirt


output_file_name = 'Resized_Upload.jpg'  # File name to save the resized image


# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Combine the directory of the script with the output filename
output_file_path = os.path.join(script_dir, output_file_name)

# Function to resize the image and save locally
def resize_image(image_path, max_size, output_path):
    with Image.open(image_path) as img:
        # Calculate the new size, keeping the aspect ratio
        ratio = min(max_size / max(img.size), 1)  # Ensure ratio never exceeds 1
        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))

        # Resize the image
        resized_img = img.resize(new_size, ImageResampling.LANCZOS if hasattr(ImageResampling, 'LANCZOS') else Image.LANCZOS)

        # Save the resized image locally
        resized_img.save(output_path, 'JPEG')

# Resize the image and save it locally
resize_image(file_path, 1024, output_file_path)

# Send the resized image to the server
files = {'file': open(output_file_path, 'rb')}
response = requests.post(url, files=files)

# Handle the MP3 file response
mp3_file_path = os.path.join(script_dir, 'response.mp3')
with open(mp3_file_path, 'wb') as f:
    f.write(response.content)

print(f"MP3 file saved to {mp3_file_path}")
