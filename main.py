from reader import extract_text_from_pdf
from speaker import speak_text, export_to_audio

PDF_PATH = "sample.pdf"

def main():
    try:
        print(f"📖 Reading PDF: {PDF_PATH}")
        start = int(input("Enter start page (1-based): "))
        end = int(input("Enter end page: "))

        full_text = extract_text_from_pdf(PDF_PATH, start_page=start, end_page=end)

        choice = input("Do you want to (1) Listen or (2) Export to audio file? Enter 1 or 2: ")

        if choice == "1":
            speak_text(full_text)
        elif choice == "2":
            output_name = input("Enter output filename (e.g. mybook.wav): ").strip()
            if not output_name.endswith(".wav"):
                output_name += ".wav"
            export_to_audio(full_text, filename=output_name)
        else:
            print("❌ Invalid choice.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
