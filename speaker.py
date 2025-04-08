import pyttsx3

def speak_text(text):
    """Convert text to speech using pyttsx3."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speaking speed
    engine.setProperty('volume', 1.0)  # Max volume
    engine.say(text)
    engine.runAndWait()
