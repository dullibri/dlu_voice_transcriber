"""Core functionality for audio recording."""
import wave
import pyaudio
from pathlib import Path

class AudioRecorder:
    """Handles audio recording from microphone."""
    
    def __init__(self, device_index=None):
        # Increased quality settings
        self.CHUNK = 4096
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 48000
        self.p = pyaudio.PyAudio()
        self.frames = []
        
        # Use specified device or find default
        self.device_index = device_index if device_index is not None else self._find_best_input_device()
        
    def _find_best_input_device(self):
        """Find the best available input device."""
        print("\nSearching for input devices...")
        
        # First, try to find the default input device
        try:
            default_device = self.p.get_default_input_device_info()
            print(f"Found default input device: {default_device['name']}")
            return default_device['index']
        except Exception:
            print("No default input device found, searching for alternatives...")
        
        # If no default device, look for any working input device
        for i in range(self.p.get_device_count()):
            try:
                device_info = self.p.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    print(f"Using input device: {device_info['name']}")
                    return i
            except Exception:
                continue
        
        raise Exception("No working input device found!")
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.p.terminate()
        
    def start_recording(self, duration: int) -> None:
        """Record audio for specified duration in seconds."""
        try:
            # Get device info for selected device
            device_info = self.p.get_device_info_by_index(self.device_index)
            print(f"\nRecording using device: {device_info['name']}")
            
            # Use device's native sample rate if possible
            try:
                native_rate = int(device_info['defaultSampleRate'])
                if native_rate > 0:
                    self.RATE = native_rate
                    print(f"Using device's native sample rate: {native_rate}Hz")
            except Exception:
                print(f"Using default sample rate: {self.RATE}Hz")
            
            stream = self.p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                input_device_index=self.device_index,
                frames_per_buffer=self.CHUNK
            )
            
            print("\nRecording started...")
            print("Please speak into the microphone...")
            
            # Calculate total chunks needed
            total_chunks = int(self.RATE / self.CHUNK * duration)
            
            # Record with progress indicator
            self.frames = []
            for i in range(total_chunks):
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                self.frames.append(data)
                if i % 10 == 0:  # Update progress every 10 chunks
                    progress = (i / total_chunks) * 100
                    print(f"Recording progress: {progress:.1f}%", end='\r')
                    
            print("\nRecording finished!")
            
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            print(f"\nError during recording: {e}")
            raise
        
    def save_wav(self, filename: str) -> Path:
        """Save recording as WAV file."""
        filepath = Path(filename)
        try:
            with wave.open(str(filepath), 'wb') as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(self.frames))
            print(f"\nSaved recording to: {filepath}")
            return filepath
        except Exception as e:
            print(f"\nError saving WAV file: {e}")
            raise

