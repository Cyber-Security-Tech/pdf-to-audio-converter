import pyttsx3

def speak_text(text):
    """Convert text to speech using pyttsx3."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

def export_to_audio(text, filename="audiobook.wav"):
    """Save text as an audio file using pyttsx3."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)

    print(f"💾 Exporting to audio file: {filename}")
    engine.save_to_file(text, filename)
    engine.runAndWait()
    print("✅ Export complete!")
