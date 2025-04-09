import PyPDF2

def extract_text_from_pdf(file_path, start_page=1, end_page=None):
    """
    Extracts text from a given page range in a PDF file.

    Parameters:
        file_path (str): Path to the PDF file.
        start_page (int): 1-based index of start page.
        end_page (int): 1-based index of end page.

    Returns:
        str: Combined text from the specified page range.

    Raises:
        ValueError: If the range is invalid or PDF can't be read.
    """
    text = ""
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)

            if start_page < 1 or (end_page and end_page < start_page):
                raise ValueError("Invalid page range.")

            start_idx = start_page - 1
            end_idx = (end_page or total_pages)

            if end_idx > total_pages:
                raise ValueError(f"PDF only has {total_pages} pages.")

            for i in range(start_idx, end_idx):
                page_text = reader.pages[i].extract_text()
                if page_text:
                    text += page_text + "\n"

    except PyPDF2.errors.PdfReadError as e:
        raise ValueError(f"PDF Read Error: {e}")
    except FileNotFoundError:
        raise ValueError("File not found. Please check the file path.")
    except Exception as e:
        raise ValueError(f"Unexpected error while reading PDF: {e}")

    if not text.strip():
        raise ValueError("No extractable text found in the selected range.")
        
    return text.strip()
