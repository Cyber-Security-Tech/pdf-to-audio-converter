# PDF to Audiobook Converter

Convert any PDF (and soon, other book formats) into realistic, chaptered audiobooks using this feature-rich Python app.

## 🎧 Features

- 📄 **PDF to Speech**: Reads aloud your selected page range
- 💾 **Export as Audio**:
  - `.wav` using offline `pyttsx3` voices
  - `.mp3` using online `gTTS` realistic voices
- 🗂️ **Chaptered Audio Export**:
  - Export each page as `chapter_1`, `chapter_2`, etc.
  - Automatically ZIPs all chapters
- 🔁 **Persistent Settings**:
  - Remembers your voice, volume, speed, export mode, etc.
- 🖥️ **Simple GUI** built with `tkinter`

## ✅ How to Use

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/pdf-to-audio.git
   cd pdf-to-audio
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python gui.py
   ```

## 📌 Requirements

- Python 3.8+
- `pyttsx3`
- `gTTS`
- `PyPDF2`
- `tkinter`

Create a `requirements.txt` like this:
```
pyttsx3
gTTS
PyPDF2
```

## 🔮 Future Enhancements

### ✅ Dark Mode Toggle
Modern UI toggle to switch themes.

### ✅ Progress Bar During Export
Visual feedback for large files or chapter exports.

### ✅ Export Bookmarks or Transcripts
Save the read text as a `.txt` or chaptered transcript.

### ✅ **Kindle Support (Planned)** 📚
Let users load Kindle books (in `.txt` or `.epub` format) and convert them to audio.

Planned workflow:
1. Allow importing `.txt` or `.epub` files
2. For `.epub`, use `ebooklib` to extract clean, readable text
3. Display extracted title and chapters
4. Use the same TTS and chapter export engine

Optional: Support importing **My Clippings.txt** from Kindle highlights.

---