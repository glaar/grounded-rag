# Grounded RAG

A RAG pipeline for document-based question answering, built to explore retrieval quality and hallucination resistance.

ref: [Lost in the Middle (Liu et al., 2023)](https://arxiv.org/pdf/2307.03172)

## Pipeline

```
PDF → chunk → embed → vector store → query → rerank → LLM answer
```

- **Chunking**: fixed-size with overlap (`CHUNK_SIZE=400`, `CHUNK_OVERLAP=100`)
- **Embedding**: `nomic-embed-text` via Ollama
- **Vector store**: ChromaDB in-memory
- **Reranking**: FlashRank — moves most relevant chunk to rank 1 before passing to LLM
- **LLM**: `qwen3:4b` via Ollama

Reranking is motivated by findings from Liu et al. (2023): LLMs perform better when relevant context appears at the start of the prompt rather than in the middle.

## Eval

Evaluated on 8 questions against a single policy document (Starbase Omega).

### Retrieval quality

|               | Precision | Recall | Hit Rate | MRR   |
|---------------|-----------|--------|----------|-------|
| Before rerank | 0.360     | 0.683  | 1.000    | 0.900 |
| After rerank  | 0.360     | 0.683  | 1.000    | 1.000 |

Reranking does not change which chunks are retrieved, only their order. The improvement in MRR (0.900 → 1.000) shows that the most relevant chunk is consistently ranked first after reranking, which matters for LLM performance (Lost in the Middle).

### Answer quality

| Category                         | Result |
|----------------------------------|--------|
| Factual accuracy (with context)  | 5/5    |
| Hallucination resistance (RAG)   | 2/3    |
| Hallucination resistance (no ctx)| 3/3    |

### Known limitations

- **Small dataset**: 5 factual and 3 unanswerable questions against one document. Results are not statistically meaningful.
- **Substring matching**: answer accuracy is measured by checking if the expected string appears in the response. This misses paraphrased correct answers and can give false negatives (e.g. the model correctly says "not in the context" but the check fails because it looks for the word "cannot").
- **Single document**: no multi-document retrieval, no chunk deduplication.
- **No semantic eval**: faithfulness and answer relevance are not measured.
