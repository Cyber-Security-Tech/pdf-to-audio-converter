"""
speaker.py

Handles all text-to-speech functionality for the PDF to Audiobook application.
Supports:
- Offline playback and export using pyttsx3 (system voices)
- Online MP3 export using Google Text-to-Speech (gTTS)
"""

import pyttsx3
from gtts import gTTS


def speak_text(text, settings=None):
    """
    Play text aloud using pyttsx3 (offline TTS).

    Parameters:
        text (str): The text to speak aloud.
        settings (dict, optional): Voice settings with keys 'voice', 'rate', 'volume'.
    """
    engine = pyttsx3.init()
    if settings:
        engine.setProperty('voice', settings.get('voice'))
        engine.setProperty('rate', settings.get('rate', 150))
        engine.setProperty('volume', settings.get('volume', 1.0))
    engine.say(text)
    engine.runAndWait()


def export_to_audio(text, filename="audiobook.wav", settings=None):
    """
    Export text to a .wav file using pyttsx3 (offline).

    Parameters:
        text (str): The text to export.
        filename (str): Output .wav filename.
        settings (dict, optional): Voice settings with keys 'voice', 'rate', 'volume'.
    """
    engine = pyttsx3.init()
    if settings:
        engine.setProperty('voice', settings.get('voice'))
        engine.setProperty('rate', settings.get('rate', 150))
        engine.setProperty('volume', settings.get('volume', 1.0))

    engine.save_to_file(text, filename)
    engine.runAndWait()


def export_to_mp3_with_gtts(text, filename="audiobook.mp3", lang="en"):
    """
    Export text to a .mp3 file using gTTS (Google Text-to-Speech).

    Parameters:
        text (str): The text to convert to speech.
        filename (str): Output .mp3 filename.
        lang (str): Language code (default is "en").

    Raises:
        RuntimeError: If gTTS fails to export the file.
    """
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
    except Exception as e:
        raise RuntimeError(f"gTTS export failed: {e}")
