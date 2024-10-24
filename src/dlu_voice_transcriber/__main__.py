"""Main entry point for the audio_to_text application."""

import argparse
from pathlib import Path
import pyaudio
from audio_to_text.core.recorder import AudioRecorder
from audio_to_text.core.transcriber import Transcriber

def list_audio_devices():
    """List all available audio input devices."""
    p = pyaudio.PyAudio()
    print("\nAvailable input devices:")
    for i in range(p.get_device_count()):
        try:
            device_info = p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:  # if it's an input device
                print(f"[{i}] {device_info['name']}")
                print(f"    Max input channels: {device_info['maxInputChannels']}")
                print(f"    Default sample rate: {device_info['defaultSampleRate']}")
        except Exception as e:
            print(f"Could not get info for device {i}: {e}")
    p.terminate()

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