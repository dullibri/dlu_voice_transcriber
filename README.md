# DLU Voice Transcriber

A Python tool for recording audio and transcribing it to text in multiple languages (English and German).

## Installation

```bash
pip install dlu_voice_transcriber
```

## Usage

List available audio devices:
```bash
dlu_transcribe --list-devices
```

Record and transcribe (replace X with your device number):
```bash
dlu_transcribe --device X --duration 5 --output my_recording
```

Example:
```bash
# List available devices
dlu_transcribe --list-devices

# Record for 10 seconds using device 2
dlu_transcribe --device 2 --duration 10 --output test_recording
```

## Features

- Record audio from any input device
- Save recordings as WAV files
- Transcribe audio to text in English and German
- Support for different audio devices
- Progress monitoring during recording

## Requirements

- Python 3.8 or higher
- Working microphone
- For Linux users: `sudo apt-get install python3-pyaudio`
- For macOS users: `brew install portaudio`

## License

This project is licensed under the MIT License - see the LICENSE file for details.