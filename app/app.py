"""
app.py

This is the main entry point for the PDF to Audiobook application.
It prompts the user to provide a PDF file path, allows selection of a page range,
extracts the text from the selected pages, and then either plays the audio aloud
or exports it to an audio file using text-to-speech.

Modules:
- reader.py: Handles text extraction from PDF
- speaker.py: Handles speech synthesis and audio export
"""

import os
import sys
import PyPDF2

from reader import extract_text_from_pdf
from speaker import speak_text, export_to_audio

def get_pdf_info(file_path):
    """
    Returns the total number of pages in a PDF.
    """
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        return len(reader.pages)


def main():
    """
    Main function that interacts with the user, processes the PDF,
    and performs text-to-speech or audio export based on user input.
    """
    try:
        # Prompt for PDF file path
        file_path = input("Enter full path to a PDF file: ").strip()

        if not os.path.isfile(file_path):
            print("Error: File does not exist.")
            sys.exit(1)
        if not file_path.lower().endswith(".pdf"):
            print("Error: File must be a PDF.")
            sys.exit(1)

        # Display page count
        total_pages = get_pdf_info(file_path)
        print(f"Loaded '{os.path.basename(file_path)}' with {total_pages} pages.")

        # Ask for page range
        start = int(input("Enter start page (1-based): "))
        end = int(input("Enter end page: "))

        if start < 1 or end < start or end > total_pages:
            print("Error: Invalid page range.")
            sys.exit(1)

        # Extract text
        full_text = extract_text_from_pdf(file_path, start_page=start, end_page=end)

        # Ask action
        print("Do you want to:")
        print("1. Listen to the audio")
        print("2. Export to an audio file")
        choice = input("Enter 1 or 2: ").strip()

        # Load voice settings
        settings = get_voice_settings()

        if choice == "1":
            speak_text(full_text, settings=settings)
        elif choice == "2":
            output_name = input("Enter output filename (e.g., mybook.wav): ").strip()
            base, ext = os.path.splitext(output_name)
            if ext.lower() != ".wav":
                output_name = f"{base}.wav"
            export_to_audio(full_text, filename=output_name, settings=settings)
            print(f"Audio saved as {output_name}")
        else:
            print("Error: Invalid choice.")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
