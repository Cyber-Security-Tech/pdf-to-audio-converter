import tkinter as tk
from tkinter import filedialog, messagebox
from reader import extract_text_from_pdf
import PyPDF2
import os

class PDFToAudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Audiobook Converter")
        self.root.geometry("500x300")

        self.pdf_path = ""
        self.total_pages = 0
        self.start_page = tk.IntVar()
        self.end_page = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Select a PDF file to begin:")
        self.label.pack(pady=10)

        self.browse_button = tk.Button(self.root, text="Browse PDF", command=self.browse_pdf)
        self.browse_button.pack()

        self.info_label = tk.Label(self.root, text="", fg="blue")
        self.info_label.pack(pady=10)

        # Page range input fields
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

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToAudioApp(root)
    root.mainloop()
