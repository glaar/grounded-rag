import pytest

import config
from utils.ingestion import chunk_text
from utils.embedding import embed_chunks
from utils.vector_store import in_memory_vector_store


SAMPLE_TEXT = """Starbase Omega is a deep-space research station located at coordinates 47.3N, 221.8E in the Kepler-22 system.
The station has 312 crew members divided into four divisions.

All crew members must undergo a full medical scan every 30 days in the medical bay on deck 4.
Crew members showing symptoms of Kepler Syndrome must report to the medical bay within 2 hours of symptom onset."""


@pytest.fixture
def sample_text() -> str:
    return SAMPLE_TEXT


@pytest.fixture(scope="module")
def chunks():
    return chunk_text(SAMPLE_TEXT, config.CHUNK_SIZE, config.CHUNK_OVERLAP)


@pytest.fixture(scope="module")
def embeddings(chunks):
    return embed_chunks(chunks)


@pytest.fixture(scope="module")
def collection(chunks, embeddings):
    return in_memory_vector_store(embeddings, chunks)
