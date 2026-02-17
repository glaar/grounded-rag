import pdfplumber


def pdf_to_text(pdf_path):
    tekst = ""
    with pdfplumber.open(pdf_path) as pdf:
        for side in pdf.pages:
            page_text = side.extract_text() or ""
            tekst += page_text + "\n"
    return tekst
