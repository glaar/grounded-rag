import pytest

import config
from utils.ingestion import chunk_text
from utils.embedding import embed_chunks
from utils.vector_store import in_memory_vector_store


SAMPLE_TEXT = """Northwind Wizardry has a strict policy on employee conduct.
All employees are expected to behave professionally at all times.

All employees must submit expense reports within 30 days of the expense.
Failure to do so will result in the expense not being reimbursed."""


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
