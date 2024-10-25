# DLU Voice Transcriber

A Python tool for recording audio and transcribing it to text in multiple languages (English and German).

## Features

- High-quality audio recording (48kHz sample rate, 16-bit depth)
- Automatic input device detection and selection
- Support for multiple audio formats (WAV, MP3)
- Configurable MP3 quality settings
- Transcription to English and German
- Progress monitoring during recording
- Save transcriptions to text files
- Detailed device information and listing
- Intelligent device selection with native sample rate support

## Installation

```bash
pip install dlu_voice_transcriber
```

### System Requirements

- Python 3.8 or higher
- Working microphone
- Linux: `sudo apt-get install python3-pyaudio portaudio19-dev`
- macOS: `brew install portaudio`
- Windows: No additional requirements

## Usage

### Basic Commands

List available audio devices:
```bash
dlu_transcribe --list-devices
```

Basic recording (5 seconds, default settings):
```bash
dlu_transcribe
```

### Advanced Usage

Record with specific settings:
```bash
dlu_transcribe --device 2 --duration 10 --output my_recording --format mp3 --mp3-quality 320 --language both --save-text
```

### Command Line Options

- `--device`: Specify input device index (shown by --list-devices)
- `--duration`: Recording duration in seconds (default: 5)
- `--output`: Output filename without extension (default: recording)
- `--format`: Output format: 'wav' or 'mp3' (default: mp3)
- `--mp3-quality`: MP3 quality in kbps (default: 320)
- `--language`: Transcription language: 'de', 'en', or 'both' (default: both)
- `--save-text`: Save transcriptions to text files
- `--list-devices`: Show available audio input devices

### Examples

List all available devices:
```bash
dlu_transcribe --list-devices
```

Record high-quality MP3 for 15 seconds:
```bash
dlu_transcribe --duration 15 --format mp3 --mp3-quality 320 --output high_quality_recording
```

Record using specific device with German-only transcription:
```bash
dlu_transcribe --device 2 --language de --save-text --output german_speech
```

## Output Files

The tool generates the following files in the `recordings` directory:
- Audio file: `<output>.<format>` (e.g., recording.mp3)
- Transcription files (if --save-text is used):
  - English: `<output>_en.txt`
  - German: `<output>_de.txt`

## License

This project is licensed under the MIT License - see the LICENSE file for details.