"""Speech recognition functionality."""
from pathlib import Path
import speech_recognition as sr

class Transcriber:
    """Handles speech-to-text conversion."""
    
    SUPPORTED_LANGUAGES = {
        'en': 'en-US',
        'de': 'de-DE'
    }
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def transcribe(self, audio_file: Path, language: str = 'en') -> str:
        """
        Transcribe audio file to text.
        
        Args:
            audio_file: Path to audio file
            language: Language code ('en' or 'de')
            
        Returns:
            Transcribed text
        """
        lang_code = self.SUPPORTED_LANGUAGES.get(language, 'en-US')
        
        with sr.AudioFile(str(audio_file)) as source:
            audio = self.recognizer.record(source)
            
        try:
            return self.recognizer.recognize_google(audio, language=lang_code)
        except sr.UnknownValueError:
            return "Speech recognition could not understand the audio"
        except sr.RequestError as e:
            return f"Could not request results from speech recognition service; {e}"
