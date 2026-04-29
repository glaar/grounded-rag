# Naive substring matching for first prototype.
# Later we can improve this with regex or semantic matching.

import config
from utils.ingestion import pdf_to_text, chunk_text
from dataset import EVAL_DATASET

raw_text = pdf_to_text(config.PDF_PATH)
chunks = chunk_text(raw_text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)

for question in EVAL_DATASET:
    answer = question["expected"].lower()
    question["chunk_with_answer"] = [i for i, chunk in enumerate(chunks) if answer in chunk.lower()] 

for question in EVAL_DATASET:
    print(question)

