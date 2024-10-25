"""Main entry point for the audio_to_text application."""

import argparse
from pathlib import Path
from dlu_voice_transcriber.core.recorder import AudioRecorder
from dlu_voice_transcriber.core.transcriber import Transcriber
import pyaudio
from pydub import AudioSegment

def list_audio_devices():
    """List all available audio input devices."""
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    
    print("\nAvailable audio input devices:")
    print("-" * 50)
    
    for i in range(num_devices):
        device_info = p.get_device_info_by_index(i)
        if device_info.get('maxInputChannels') > 0:  # Only show input devices
            print(f"Device ID {i}: {device_info.get('name')}")
            print(f"    Input channels: {device_info.get('maxInputChannels')}")
            print(f"    Sample rate: {int(device_info.get('defaultSampleRate'))}Hz")
            print(f"    Default: {'Yes' if i == p.get_default_input_device_info()['index'] else 'No'}")
            print("-" * 50)
    
    p.terminate()

def save_transcription(text: str, output_dir: Path, filename: str, language: str):
    """Save transcription to a text file."""
    transcript_file = output_dir / f"{filename}_{language}.txt"
    with open(transcript_file, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Saved {language} transcription to: {transcript_file}")

def main():
    parser = argparse.ArgumentParser(description='Record audio and transcribe to text.')
    parser.add_argument('--duration', type=int, default=5,
                       help='Recording duration in seconds')
    parser.add_argument('--output', type=str, default='recording',
                       help='Output filename (without extension)')
    parser.add_argument('--format', type=str, choices=['wav', 'mp3'], default='mp3',
                       help='Output audio format (default: mp3)')
    parser.add_argument('--mp3-quality', type=int, default=320,
                       help='MP3 quality in kbps (default: 320)')
    parser.add_argument('--language', type=str, choices=['de', 'en', 'both'], default='both',
                       help='Language for transcription: de (German), en (English), or both (default: both)')
    parser.add_argument('--list-devices', action='store_true',
                       help='List available audio input devices and exit')
    parser.add_argument('--device', type=int,
                       help='Specify input device index to use')
    parser.add_argument('--save-text', action='store_true',
                       help='Save transcriptions to text files')
    
    args = parser.parse_args()
    
    if args.list_devices:
        list_audio_devices()
        return
    
    output_dir = Path('recordings')
    output_dir.mkdir(exist_ok=True)
    
    # Create output filename with appropriate extension
    output_file = output_dir / f"{args.output}.{args.format}"
    
    try:
        with AudioRecorder(device_index=args.device) as recorder:
            # Record audio
            recorder.start_recording(args.duration)
            
            # Save in requested format
            if args.format == 'mp3':
                audio_file = recorder.save_mp3(output_file, quality=args.mp3_quality)
            else:
                audio_file = recorder.save_wav(output_file)
        
        # For transcription, we need a WAV file
        transcription_file = None
        if args.format == 'mp3':
            # Convert back to WAV temporarily for transcription
            transcription_file = output_dir / f"{args.output}_temp.wav"
            audio = AudioSegment.from_mp3(str(audio_file))
            audio.export(str(transcription_file), format="wav")
        else:
            transcription_file = audio_file
        
        # Transcribe
        transcriber = Transcriber()
        
        # Dictionary to store transcriptions
        transcriptions = {}
        
        # Handle English transcription
        if args.language in ['en', 'both']:
            print("\nEnglish transcription:")
            text_en = transcriber.transcribe(transcription_file, 'en')
            print(text_en)
            transcriptions['en'] = text_en
            
            if args.save_text:
                save_transcription(text_en, output_dir, args.output, 'en')
        
        # Handle German transcription
        if args.language in ['de', 'both']:
            print("\nGerman transcription:")
            text_de = transcriber.transcribe(transcription_file, 'de')
            print(text_de)
            transcriptions['de'] = text_de
            
            if args.save_text:
                save_transcription(text_de, output_dir, args.output, 'de')
        
        # Clean up temporary WAV file if we created one
        if args.format == 'mp3' and transcription_file and transcription_file.exists():
            transcription_file.unlink()
            
    except Exception as e:
        print(f"\nError: {e}")
        return

if __name__ == "__main__":
    main()