import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from reader import extract_text_from_pdf
from speaker import speak_text, export_to_audio, export_to_mp3_with_gtts
import PyPDF2
import pyttsx3
import threading
import os
import zipfile
import json

SETTINGS_FILE = "settings.json"

class PDFToAudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Audiobook Converter")
        self.root.geometry("600x620")

        self.pdf_path = ""
        self.total_pages = 0
        self.start_page = tk.IntVar()
        self.end_page = tk.IntVar()

        self.voices = []
        self.voice_choice = tk.StringVar()
        self.speech_rate = tk.IntVar(value=150)
        self.volume = tk.DoubleVar(value=1.0)

        self.export_mode = tk.StringVar(value="Offline (WAV)")
        self.chapter_export = tk.BooleanVar(value=False)

        self.engine = pyttsx3.init()
        self.speaking_thread = None

        self.create_widgets()
        self.load_voices()
        self.load_settings()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Select a PDF file to begin:")
        self.label.pack(pady=10)

        self.browse_button = tk.Button(self.root, text="Browse PDF", command=self.browse_pdf)
        self.browse_button.pack()

        self.info_label = tk.Label(self.root, text="", fg="blue")
        self.info_label.pack(pady=10)

        self.range_frame = tk.Frame(self.root)
        self.range_frame.pack(pady=10)

        tk.Label(self.range_frame, text="Start Page:").grid(row=0, column=0, padx=5)
        self.start_entry = tk.Entry(self.range_frame, textvariable=self.start_page, width=5)
        self.start_entry.grid(row=0, column=1)

        tk.Label(self.range_frame, text="End Page:").grid(row=0, column=2, padx=5)
        self.end_entry = tk.Entry(self.range_frame, textvariable=self.end_page, width=5)
        self.end_entry.grid(row=0, column=3)

        self.validate_button = tk.Button(self.root, text="Validate Page Range", command=self.validate_range)
        self.validate_button.pack(pady=5)

        tk.Label(self.root, text="Select Voice:").pack(pady=(15, 0))
        self.voice_dropdown = ttk.Combobox(self.root, textvariable=self.voice_choice, state="readonly", width=50)
        self.voice_dropdown.pack()

        tk.Label(self.root, text="Speech Rate (100–300):").pack(pady=(15, 0))
        self.rate_slider = tk.Scale(self.root, from_=100, to=300, orient="horizontal", variable=self.speech_rate)
        self.rate_slider.pack()

        tk.Label(self.root, text="Volume (0.0 to 1.0):").pack(pady=(15, 0))
        self.volume_slider = tk.Scale(self.root, from_=0.0, to=1.0, resolution=0.1,
                                      orient="horizontal", variable=self.volume)
        self.volume_slider.pack()

        tk.Label(self.root, text="Export Mode:").pack(pady=(15, 0))
        self.export_mode_dropdown = ttk.Combobox(self.root, textvariable=self.export_mode, state="readonly", width=30)
        self.export_mode_dropdown["values"] = ["Offline (WAV)", "Online (MP3)"]
        self.export_mode_dropdown.current(0)
        self.export_mode_dropdown.pack()

        self.chapter_checkbox = tk.Checkbutton(self.root, text="Export each page as a separate chapter",
                                               variable=self.chapter_export)
        self.chapter_checkbox.pack(pady=5)

        # Buttons: Play, Stop, Export
        self.actions_frame = tk.Frame(self.root)
        self.actions_frame.pack(pady=20)

        self.play_button = tk.Button(self.actions_frame, text="Play Audio", command=self.start_speaking_thread, width=15)
        self.play_button.grid(row=0, column=0, padx=10)

        self.stop_button = tk.Button(self.actions_frame, text="Stop Audio", command=self.stop_speaking, width=15)
        self.stop_button.grid(row=0, column=1, padx=10)

        self.export_button = tk.Button(self.actions_frame, text="Export", command=self.export_audio, width=15)
        self.export_button.grid(row=0, column=2, padx=10)

    def load_voices(self):
        self.voices = self.engine.getProperty("voices")
        voice_names = []

        for v in self.voices:
            lang = v.languages[0] if hasattr(v, 'languages') and v.languages else "Unknown"
            voice_names.append(f"{v.name} ({lang})")

        self.voice_dropdown["values"] = voice_names
        if voice_names:
            self.voice_dropdown.current(0)
            self.voice_choice.set(voice_names[0])

    def load_settings(self):
        if not os.path.exists(SETTINGS_FILE):
            return
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
            self.voice_choice.set(data.get("voice", self.voice_choice.get()))
            self.speech_rate.set(data.get("rate", 150))
            self.volume.set(data.get("volume", 1.0))
            self.export_mode.set(data.get("export_mode", "Offline (WAV)"))
            self.chapter_export.set(data.get("chapter_export", False))
            self.start_page.set(data.get("start_page", 1))
            self.end_page.set(data.get("end_page", 1))
            print("✅ Settings loaded.")
        except Exception as e:
            print("❌ Could not load settings:", e)

    def save_settings(self):
        data = {
            "voice": self.voice_choice.get(),
            "rate": self.speech_rate.get(),
            "volume": self.volume.get(),
            "export_mode": self.export_mode.get(),
            "chapter_export": self.chapter_export.get(),
            "start_page": self.start_page.get(),
            "end_page": self.end_page.get()
        }
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(data, f, indent=4)
            print("✅ Settings saved.")
        except Exception as e:
            messagebox.showerror("Settings Save Failed", f"Error: {e}")
            print("❌ Could not save settings:", e)

    def browse_pdf(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")],
            title="Select a PDF File"
        )
        if file_path:
            try:
                with open(file_path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    self.total_pages = len(reader.pages)
                    self.pdf_path = file_path
                    file_name = os.path.basename(file_path)
                    self.info_label.config(
                        text=f"✅ Loaded '{file_name}' ({self.total_pages} pages)"
                    )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read PDF: {e}")
                self.info_label.config(text="")

    def validate_range(self):
        try:
            start = self.start_page.get()
            end = self.end_page.get()

            if not self.pdf_path:
                raise ValueError("Please select a PDF first.")
            if start < 1 or end < start or end > self.total_pages:
                raise ValueError("Invalid page range.")
            messagebox.showinfo("Success", f"Valid range: pages {start} to {end}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_voice_settings(self):
        selected_voice_name = self.voice_choice.get()
        selected_voice_obj = next((v for v in self.voices if v.name in selected_voice_name), self.voices[0])
        return {
            "voice": selected_voice_obj.id,
            "rate": self.speech_rate.get(),
            "volume": self.volume.get()
        }

    def start_speaking_thread(self):
        if self.speaking_thread and self.speaking_thread.is_alive():
            messagebox.showwarning("Speaking", "Audio is already playing.")
            return
        self.speaking_thread = threading.Thread(target=self.speak_text, daemon=True)
        self.speaking_thread.start()

    def speak_text(self):
        try:
            text = extract_text_from_pdf(self.pdf_path, self.start_page.get(), self.end_page.get())
            settings = self.get_voice_settings()
            self.engine.setProperty('voice', settings['voice'])
            self.engine.setProperty('rate', settings['rate'])
            self.engine.setProperty('volume', settings['volume'])
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def stop_speaking(self):
        try:
            self.engine.stop()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop audio: {e}")

    def export_audio(self):
        try:
            start = self.start_page.get()
            end = self.end_page.get()
            export_each = self.chapter_export.get()
            export_mode = self.export_mode.get()
            settings = self.get_voice_settings()

            self.save_settings()

            if export_each:
                output_dir = filedialog.askdirectory(title="Select Folder to Save Chapters")
                if not output_dir:
                    return

                filenames = []
                for i in range(start, end + 1):
                    text = extract_text_from_pdf(self.pdf_path, i, i)
                    ext = "mp3" if "MP3" in export_mode else "wav"
                    filename = os.path.join(output_dir, f"chapter_{i}.{ext}")
                    filenames.append(filename)

                    if "MP3" in export_mode:
                        export_to_mp3_with_gtts(text, filename=filename)
                    else:
                        export_to_audio(text, filename=filename, settings=settings)

                zip_path = os.path.join(output_dir, "chapters.zip")
                with zipfile.ZipFile(zip_path, "w") as zipf:
                    for file in filenames:
                        zipf.write(file, arcname=os.path.basename(file))

                messagebox.showinfo("Export Complete", f"Chapters saved and zipped:\n{zip_path}")

            else:
                text = extract_text_from_pdf(self.pdf_path, start, end)
                if "MP3" in export_mode:
                    output_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                               filetypes=[("MP3 files", "*.mp3")],
                                                               title="Save MP3 As")
                    if output_path:
                        export_to_mp3_with_gtts(text, filename=output_path)
                        messagebox.showinfo("Export Complete", f"Audio saved to:\n{output_path}")
                else:
                    output_path = filedialog.asksaveasfilename(defaultextension=".wav",
                                                               filetypes=[("WAV files", "*.wav")],
                                                               title="Save WAV As")
                    if output_path:
                        export_to_audio(text, filename=output_path, settings=settings)
                        messagebox.showinfo("Export Complete", f"Audio saved to:\n{output_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToAudioApp(root)
    root.mainloop()
