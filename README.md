# Audio File Converter

A simple Python tool to convert audio files between different formats.

## Features

- Convert between multiple audio formats (MP3, WAV, OGG, FLAC, AAC, M4A, WMA, AIFF)
- Simple command-line interface
- Preserves audio quality during conversion

## Requirements

- Python 3.6+
- pydub library
- ffmpeg (must be installed on your system)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install ffmpeg:
   - **Windows**: Download from https://ffmpeg.org/download.html or use `choco install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` or `sudo yum install ffmpeg`

## Usage

### Web Application

1. Start the Flask backend:
```bash
python app.py
```

2. In a separate terminal, start the Next.js frontend:
```bash
cd nextjs-frontend
npm install
npm run dev
```

3. Open your browser to http://localhost:3000

### Command Line

Basic syntax:
```bash
python audio_converter.py <input_file> <output_file>
```

### Examples

Convert MP3 to WAV:
```bash
python audio_converter.py song.mp3 song.wav
```

Convert FLAC to MP3:
```bash
python audio_converter.py audio.flac audio.mp3
```

Convert WAV to OGG:
```bash
python audio_converter.py recording.wav recording.ogg
```

## Supported Formats

- MP3
- WAV
- OGG
- FLAC
- AAC
- M4A
- WMA
- AIFF

## Notes

- The output format is automatically detected from the output filename extension
- Make sure ffmpeg is properly installed and accessible from your PATH
- Large files may take some time to convert
