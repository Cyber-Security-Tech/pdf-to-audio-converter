import tkinter as tk
from tkinter import filedialog, messagebox
from reader import extract_text_from_pdf
import PyPDF2
import os

class PDFToAudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Audiobook Converter")
        self.root.geometry("500x250")

        self.pdf_path = ""
        self.total_pages = 0

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Select a PDF file to begin:")
        self.label.pack(pady=10)

        self.browse_button = tk.Button(self.root, text="Browse PDF", command=self.browse_pdf)
        self.browse_button.pack()

        self.info_label = tk.Label(self.root, text="", fg="blue")
        self.info_label.pack(pady=10)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToAudioApp(root)
    root.mainloop()
