"""Main entry point for the dlu_voice_transcriber application."""

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
    parser.add_argument('--list-devices', action='store_true',
                       help='List available audio input devices and exit')
    parser.add_argument('--device', type=int,
                       help='Specify input device index to use')
    args = parser.parse_args()
    
    if args.list_devices:
        list_audio_devices()
        return
    
    output_dir = Path('recordings')
    output_dir.mkdir(exist_ok=True)
    
    wav_file = output_dir / f"{args.output}.wav"
    
    try:
        with AudioRecorder(device_index=args.device) as recorder:
            # Record audio
            recorder.start_recording(args.duration)
            
            # Save as WAV
            recorder.save_wav(wav_file)
        
        # Transcribe
        transcriber = Transcriber()
        
        print("\nEnglish transcription:")
        text_en = transcriber.transcribe(wav_file, 'en')
        print(text_en)
        
        print("\nGerman transcription:")
        text_de = transcriber.transcribe(wav_file, 'de')
        print(text_de)
        
    except Exception as e:
        print(f"\nError: {e}")
        return

if __name__ == "__main__":
    main()