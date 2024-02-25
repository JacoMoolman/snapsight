from flask import Flask, request, send_from_directory
import os
from werkzeug.utils import secure_filename
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = '/workspace/uploaded_image'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        
        # Use the local script for TTS. The script handles output file location.
        subprocess.run(["/workspace/tts.sh", description], check=True)

        # Convert WAV to MP3
        wav_path = '/workspace/output.wav'  # TTS script output
        mp3_path = os.path.join(app.config['UPLOAD_FOLDER'], secured_filename.rsplit('.', 1)[0] + '.mp3')
        subprocess.run(['ffmpeg', '-y', '-i', wav_path, '-codec:a', 'libmp3lame', mp3_path], check=True)

        # Return the MP3 file in the response
        print(mp3_path)
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path=os.path.basename(mp3_path), as_attachment=True)

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
    app.run(debug=True, host='0.0.0.0', port=5210)
