from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import os
from werkzeug.utils import secure_filename
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Directory to temporarily store audio files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        logger.error("No audio file provided")
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    filename = secure_filename(audio_file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Check if file is empty
    audio_file.seek(0, os.SEEK_END)
    if audio_file.tell() == 0:
        logger.error("Received empty audio file")
        return jsonify({'error': 'Audio file is empty'}), 400
    audio_file.seek(0)  # Reset file pointer
    
    try:
        audio_file.save(filepath)
        logger.info(f"Saved audio file to {filepath}")
        
        # Verify file exists and is readable
        if not os.path.exists(filepath):
            logger.error("Saved file does not exist")
            return jsonify({'error': 'Failed to save audio file'}), 500
            
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        try:
            with sr.AudioFile(filepath) as source:
                audio = recognizer.record(source)
            # Transcribe audio using Google's API
            text = recognizer.recognize_google(audio)
            logger.info("Transcription successful")
            return jsonify({'text': text})
        finally:
            # Clean up the audio file
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Deleted audio file {filepath}")
                
    except sr.UnknownValueError:
        logger.error("Speech recognition could not understand the audio")
        return jsonify({'error': 'Could not understand the audio'}), 400
    except sr.RequestError as e:
        logger.error(f"Speech recognition error: {str(e)}")
        return jsonify({'error': f'Speech recognition error: {str(e)}'}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)