"""Core functionality for audio recording and transcription."""

from .recorder import AudioRecorder
from .transcriber import Transcriber

__all__ = ['AudioRecorder', 'Transcriber']

# File: audio_to_text/__init__.py
# This file can remain empty

# File: audio_to_text/__main__.py
"""Main entry point for the audio_to_text application."""

import argparse
from pathlib import Path
from dlu_voice_transcriber.core.recorder import AudioRecorder
from dlu_voice_transcriber.core.transcriber import Transcriber

def main():
    parser = argparse.ArgumentParser(description='Record audio and transcribe to text.')
    parser.add_argument('--duration', type=int, default=5,
                       help='Recording duration in seconds')
    parser.add_argument('--output', type=str, default='recording',
                       help='Output filename (without extension)')
    args = parser.parse_args()
    
    output_dir = Path('recordings')
    output_dir.mkdir(exist_ok=True)
    
    wav_file = output_dir / f"{args.output}.wav"
    mp3_file = output_dir / f"{args.output}.mp3"
    
    with AudioRecorder() as recorder:
        # Record audio
        recorder.start_recording(args.duration)
        
        # Save as WAV
        recorder.save_wav(wav_file)
        
        # Convert to MP3
        recorder.convert_to_mp3(wav_file, mp3_file)
    
    # Transcribe
    transcriber = Transcriber()
    
    print("\nEnglish transcription:")
    text_en = transcriber.transcribe(wav_file, 'en')
    print(text_en)
    
    print("\nGerman transcription:")
    text_de = transcriber.transcribe(wav_file, 'de')
    print(text_de)
    
    # Clean up WAV file
    wav_file.unlink()

if __name__ == "__main__":
    main()