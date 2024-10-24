"""Core functionality for audio recording."""
import wave
import pyaudio
from pathlib import Path
from pydub import AudioSegment

class AudioRecorder:
    """Handles audio recording from microphone."""
    
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.p = pyaudio.PyAudio()
        self.frames = []
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.p.terminate()
        
    def start_recording(self, duration: int) -> None:
        """Record audio for specified duration in seconds."""
        stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        print("Recording started...")
        
        for _ in range(0, int(self.RATE / self.CHUNK * duration)):
            data = stream.read(self.CHUNK)
            self.frames.append(data)
            
        print("Recording finished")
        
        stream.stop_stream()
        stream.close()
        
    def save_wav(self, filename: str) -> Path:
        """Save recording as WAV file."""
        filepath = Path(filename)
        with wave.open(str(filepath), 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.frames))
        return filepath
        
    def convert_to_mp3(self, wav_file: Path, mp3_file: Path) -> Path:
        """Convert WAV to MP3 format."""
        audio = AudioSegment.from_wav(str(wav_file))
        audio.export(str(mp3_file), format="mp3")
        return mp3_file
