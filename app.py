#!/usr/bin/env python3
"""
Flask API for audio file conversion
"""

import os
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from pathlib import Path
from pydub import AudioSegment
import tempfile
import shutil

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()

ALLOWED_FORMATS = ['mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a', 'wma', 'aiff', 'webm']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FORMATS


@app.route('/convert', methods=['POST'])
def convert():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['audio_file']
    output_format = request.form.get('output_format', 'mp3').lower()
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file format'}), 400
    
    if output_format not in ALLOWED_FORMATS:
        return jsonify({'error': 'Invalid output format'}), 400
    
    input_path = None
    output_path = None
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        # Get input format
        input_format = filename.rsplit('.', 1)[1].lower()
        
        # Create output filename
        base_name = filename.rsplit('.', 1)[0]
        output_filename = f"{base_name}.{output_format}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Convert audio
        audio = AudioSegment.from_file(input_path, format=input_format)
        audio.export(output_path, format=output_format)
        
        # Clean up input file (don't delete yet, might be in use)
        try:
            os.remove(input_path)
        except PermissionError:
            pass  # File will be cleaned up later by temp folder cleanup
        
        return send_file(
            output_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype=f'audio/{output_format}'
        )
    
    except Exception as e:
        # Log the full error for debugging
        print(f"Conversion error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Clean up files on error
        try:
            if input_path and os.path.exists(input_path):
                os.remove(input_path)
            if output_path and os.path.exists(output_path):
                os.remove(output_path)
        except PermissionError:
            pass  # File cleanup will happen later
        return jsonify({'error': str(e)}), 500


@app.route('/convert-batch', methods=['POST'])
def convert_batch():
    if 'audio_files' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400
    
    files = request.files.getlist('audio_files')
    output_format = request.form.get('output_format', 'mp3').lower()
    
    if not files or len(files) == 0:
        return jsonify({'error': 'No files selected'}), 400
    
    if output_format not in ALLOWED_FORMATS:
        return jsonify({'error': 'Invalid output format'}), 400
    
    converted_files = []
    errors = []
    
    for file in files:
        if file.filename == '' or not allowed_file(file.filename):
            errors.append(f"{file.filename}: Invalid file")
            continue
        
        input_path = None
        output_path = None
        
        try:
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)
            
            input_format = filename.rsplit('.', 1)[1].lower()
            base_name = filename.rsplit('.', 1)[0]
            output_filename = f"{base_name}.{output_format}"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            audio = AudioSegment.from_file(input_path, format=input_format)
            audio.export(output_path, format=output_format)
            
            converted_files.append(output_path)
            
            try:
                os.remove(input_path)
            except PermissionError:
                pass
                
        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")
            try:
                if input_path and os.path.exists(input_path):
                    os.remove(input_path)
                if output_path and os.path.exists(output_path):
                    os.remove(output_path)
            except PermissionError:
                pass
    
    if not converted_files:
        return jsonify({'error': 'All conversions failed', 'details': errors}), 500
    
    # Create zip file
    import zipfile
    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], 'converted_files.zip')
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file_path in converted_files:
            zipf.write(file_path, os.path.basename(file_path))
    
    # Clean up converted files
    for file_path in converted_files:
        try:
            os.remove(file_path)
        except PermissionError:
            pass
    
    response = {
        'success': True,
        'converted': len(converted_files),
        'errors': errors
    }
    
    return send_file(
        zip_path,
        as_attachment=True,
        download_name='converted_files.zip',
        mimetype='application/zip'
    )


@app.route('/')
def index():
    return jsonify({
        'message': 'Audio Converter API',
        'endpoints': {
            'POST /convert': 'Convert audio files',
            'GET /formats': 'Get supported formats'
        }
    })


@app.route('/formats')
def get_formats():
    return jsonify({'formats': ALLOWED_FORMATS})


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print("Starting Audio Converter Web App...")
    print(f"Running on port: {port}")
    app.run(debug=False, host='0.0.0.0', port=port)
