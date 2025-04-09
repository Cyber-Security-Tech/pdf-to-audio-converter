import os
from reader import extract_text_from_pdf
from speaker import speak_text, export_to_audio, get_voice_settings
import PyPDF2

def get_pdf_info(file_path):
    """Returns total number of pages in a PDF."""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        return len(reader.pages)

def main():
    try:
        # Prompt for PDF file path
        file_path = input("Enter full path to a PDF file: ").strip()

        if not os.path.isfile(file_path):
            raise ValueError("File does not exist.")
        if not file_path.lower().endswith(".pdf"):
            raise ValueError("File must be a PDF.")

        # Show page count
        total_pages = get_pdf_info(file_path)
        print(f"✅ Loaded '{os.path.basename(file_path)}' with {total_pages} pages.")

        # Ask for page range
        start = int(input("Enter start page (1-based): "))
        end = int(input("Enter end page: "))

        if start < 1 or end < start or end > total_pages:
            raise ValueError("Invalid page range.")

        # Extract and process
        full_text = extract_text_from_pdf(file_path, start_page=start, end_page=end)

        # Ask action
        choice = input("Do you want to (1) Listen or (2) Export to audio file? Enter 1 or 2: ")

        # Get voice settings
        settings = get_voice_settings()

        if choice == "1":
            speak_text(full_text, settings=settings)
        elif choice == "2":
            output_name = input("Enter output filename (e.g. mybook.wav): ").strip()
            if not output_name.endswith(".wav"):
                output_name += ".wav"
            export_to_audio(full_text, filename=output_name, settings=settings)
        else:
            print("❌ Invalid choice.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
