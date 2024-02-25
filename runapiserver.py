from flask import Flask, request, send_from_directory
import os
import base64
import requests
from werkzeug.utils import secure_filename
import boto3
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = '/workspace/uploaded_image'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
AWS_ACCESS_KEY_ID = '3NC948C37N0C93478340N'
AWS_SECRET_ACCESS_KEY = 'kP+xtXCo/9qHd3K+DFGTTgfdfdGrtdtrY'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Polly client
polly_client = boto3.client(
    'polly',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-west-2'
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        raw_filename = os.path.basename(file.filename)
        secured_filename = secure_filename(raw_filename)
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], secured_filename)
        file.save(saved_path)

        # Process the image and get description
        description = get_image_description(saved_path)
        
        # Synthesize speech
        response = polly_client.synthesize_speech(
            Text=description,
            OutputFormat='mp3',
            VoiceId='Danielle',
            Engine='neural'
        )

        # Save the audio stream to a file in the UPLOAD_FOLDER
        audio_filename = secured_filename.rsplit('.', 1)[0] + '.mp3'
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
        with open(audio_path, 'wb') as audio_file:
            audio_file.write(response['AudioStream'].read())

        # Return the MP3 file in the response
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path=audio_filename, as_attachment=True)

    else:
        return 'File type not allowed'

def get_image_description(image_path):
    try:
        # Construct the command to run the external script with the image path
        command = ["python", "/workspace/llavainf.py", image_path]
        
        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Extract the script's output (description of the image)
        description = result.stdout.strip()
        
        return description
    except subprocess.CalledProcessError as e:
        # If the script execution fails, return an error message
        return f"Error in processing the image: {e}"


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5210)
