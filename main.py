from reader import extract_text_from_pdf
from speaker import speak_text

PDF_PATH = "sample.pdf"

def main():
    try:
        print(f"📖 Reading PDF: {PDF_PATH}")

        # Ask for page range
        start = int(input("Enter start page (1-based): "))
        end = int(input("Enter end page: "))

        # Extract text from range
        full_text = extract_text_from_pdf(PDF_PATH, start_page=start, end_page=end)
        print("🔊 Speaking text...")
        speak_text(full_text)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
