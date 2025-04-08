import PyPDF2

def extract_text_from_pdf(file_path):
    """
    Extracts all text from the given PDF file.

    Parameters:
        file_path (str): Path to the PDF file.

    Returns:
        str: Combined text from all pages.

    Raises:
        ValueError: If the file cannot be read or is not a valid PDF.
    """
    text = ""
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            if not reader.pages:
                raise ValueError("PDF file has no readable pages.")
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except PyPDF2.errors.PdfReadError as e:
        raise ValueError(f"PDF Read Error: {e}")
    except FileNotFoundError:
        raise ValueError("File not found. Please check the file path.")
    except Exception as e:
        raise ValueError(f"Unexpected error while reading PDF: {e}")
    
    if not text.strip():
        raise ValueError("No extractable text found in the PDF.")
        
    return text.strip()

