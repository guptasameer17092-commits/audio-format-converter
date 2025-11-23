#!/usr/bin/env python3
"""
Audio File Converter
Converts audio files from any format to any format
"""

import os
import sys
from pathlib import Path

try:
    from pydub import AudioSegment
except ImportError:
    print("Error: pydub is not installed.")
    print("Install it with: pip install pydub")
    print("Note: You also need ffmpeg installed on your system")
    sys.exit(1)


def get_supported_formats():
    """Returns list of commonly supported audio formats"""
    return ['mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a', 'wma', 'aiff']


def convert_audio(input_file, output_file, output_format=None):
    """
    Convert audio file from one format to another
    
    Args:
        input_file: Path to input audio file
        output_file: Path to output audio file
        output_format: Output format (optional, inferred from output_file if not provided)
    """
    input_path = Path(input_file)
    output_path = Path(output_file)
    
    # Validate input file exists
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Determine input format
    input_format = input_path.suffix[1:].lower()
    
    # Determine output format
    if output_format is None:
        output_format = output_path.suffix[1:].lower()
    
    if not output_format:
        raise ValueError("Output format must be specified either in filename or as parameter")
    
    print(f"Converting {input_file} ({input_format}) to {output_file} ({output_format})...")
    
    # Load audio file
    try:
        audio = AudioSegment.from_file(input_file, format=input_format)
    except Exception as e:
        raise Exception(f"Failed to load audio file: {e}")
    
    # Export to new format
    try:
        audio.export(output_file, format=output_format)
        print(f"✓ Conversion successful! Output saved to: {output_file}")
    except Exception as e:
        raise Exception(f"Failed to export audio file: {e}")


def main():
    if len(sys.argv) < 3:
        print("Audio File Converter")
        print("=" * 50)
        print("\nUsage:")
        print("  python audio_converter.py <input_file> <output_file>")
        print("\nExample:")
        print("  python audio_converter.py song.mp3 song.wav")
        print("  python audio_converter.py audio.flac audio.mp3")
        print(f"\nSupported formats: {', '.join(get_supported_formats())}")
        print("\nNote: Requires ffmpeg to be installed on your system")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        convert_audio(input_file, output_file)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
