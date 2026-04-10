import pdfplumber


def pdf_to_text(pdf_path):
    tekst = ""
    with pdfplumber.open(pdf_path) as pdf:
        for side in pdf.pages:
            page_text = side.extract_text() or ""
            tekst += page_text + "\n"
    return tekst


def get_paragraphs(text):
    paragraphs = []
    for line in text.splitlines():
        trimmed_line = line.strip()
        if trimmed_line:
            paragraphs.append(trimmed_line)
    return paragraphs


def chunk_text(text, max_size, overlap):
    paragraphs = get_paragraphs(text)

    pending_tail = None
    chunks = []
    chunk_parts = []
    current_length = 0

    for paragraph in paragraphs:

        if pending_tail is not None:
            chunk_parts = [pending_tail]
            current_length = len(pending_tail)
            pending_tail = None

        separator_length = 1 if chunk_parts else 0
        next_length = current_length + separator_length + len(paragraph)

        # paragraphs longer than max_size are added as-is; revisit after eval
        if len(paragraph) > max_size:
            chunks.append(paragraph)
        elif next_length <= max_size:
            chunk_parts.append(paragraph)
            current_length = next_length
        else:
            chunk_parts.append(paragraph)
            chunks.append("\n".join(chunk_parts))
            pending_tail = chunks[-1][-overlap:] if overlap > 0 else None
            chunk_parts = []
            current_length = 0

    if chunk_parts:
        chunks.append("\n".join(chunk_parts))

    return chunks
