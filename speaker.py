import pyttsx3
from gtts import gTTS

def speak_text(text, settings=None):
    """Play text aloud using pyttsx3 (offline)."""
    engine = pyttsx3.init()
    if settings:
        engine.setProperty('voice', settings['voice'])
        engine.setProperty('rate', settings['rate'])
        engine.setProperty('volume', settings['volume'])
    engine.say(text)
    engine.runAndWait()

def export_to_audio(text, filename="audiobook.wav", settings=None):
    """Export text to .wav file using pyttsx3 (offline)."""
    engine = pyttsx3.init()
    if settings:
        engine.setProperty('voice', settings['voice'])
        engine.setProperty('rate', settings['rate'])
        engine.setProperty('volume', settings['volume'])

    engine.save_to_file(text, filename)
    engine.runAndWait()

def export_to_mp3_with_gtts(text, filename="audiobook.mp3", lang="en"):
    """Export text to .mp3 using gTTS (online, realistic voice)."""
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
    except Exception as e:
        raise RuntimeError(f"gTTS export failed: {e}")
