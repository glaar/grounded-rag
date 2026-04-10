from utils.ingestion import chunk_text, get_paragraphs

MAX_SIZE = 30
OVERLAP = 20

def test_all_paragraphs_contained_in_chunks(sample_text):
    paragraphs = get_paragraphs(sample_text)
    chunks = chunk_text(sample_text, max_size=MAX_SIZE, overlap=OVERLAP)

    all_chunks = "\n".join(chunks)
    for paragraph in paragraphs:
        assert paragraph in all_chunks, "Paragraph is missing from chunks"


def test_no_empty_chunks(sample_text):
    chunks = chunk_text(sample_text, max_size=MAX_SIZE, overlap=OVERLAP)

    for chunk in chunks:
        assert chunk != "", "Chunk should not be empty"


def test_no_chunks_on_empty_string():
    chunks = chunk_text("", max_size=MAX_SIZE, overlap=OVERLAP)
    assert len(chunks) == 0, "Expected no chunks for empty string"

def test_overlap(sample_text):
    chunks = chunk_text(sample_text, max_size=MAX_SIZE, overlap=OVERLAP)

    for i in range(1, len(chunks)):
        tail = chunks[i-1][-OVERLAP:]
        assert tail in chunks[i]

def test_single_paragraph():
    sample_text = "This is a single paragraph"

    chunks = chunk_text(sample_text, max_size=MAX_SIZE, overlap=OVERLAP)
    assert len(chunks) == 1, "Number of chunks should be one"
