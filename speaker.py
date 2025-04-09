import pyttsx3

def speak_text(text, settings=None):
    """Convert text to speech using pyttsx3."""
    engine = pyttsx3.init()
    if settings:
        engine.setProperty('voice', settings['voice'])
        engine.setProperty('rate', settings['rate'])
        engine.setProperty('volume', settings['volume'])
    engine.say(text)
    engine.runAndWait()

def export_to_audio(text, filename="audiobook.wav", settings=None):
    """Save text as an audio file using pyttsx3."""
    engine = pyttsx3.init()
    if settings:
        engine.setProperty('voice', settings['voice'])
        engine.setProperty('rate', settings['rate'])
        engine.setProperty('volume', settings['volume'])

    print(f"💾 Exporting to audio file: {filename}")
    engine.save_to_file(text, filename)
    engine.runAndWait()
    print("✅ Export complete!")

def get_voice_settings():
    """Prompt the user for voice, rate, and volume settings."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    print("\n🗣️ Available Voices:")
    for idx, voice in enumerate(voices):
        print(f"{idx + 1}: {voice.name} ({voice.languages})")

    try:
        voice_choice = int(input("Choose a voice (number): ")) - 1
        if not (0 <= voice_choice < len(voices)):
            raise ValueError("Invalid voice selection.")
    except ValueError:
        print("❌ Invalid voice choice. Using default.")
        voice_choice = 0

    try:
        rate = int(input("Set speech rate (default 150, range 100–300): "))
    except ValueError:
        rate = 150

    try:
        volume = float(input("Set volume (0.0 to 1.0, default 1.0): "))
        if not (0.0 <= volume <= 1.0):
            raise ValueError
    except:
        volume = 1.0

    return {
        "voice": voices[voice_choice].id,
        "rate": rate,
        "volume": volume
    }
