EVAL_DATASET = [
    {
        "question": "How many crew members does Starbase Omega have?",
        "expected": "312",
        "chunk_with_answer": [0],
    },
    {
        "question": "What is the water recycling efficiency rate on the station?",
        "expected": "97.3%",
        "chunk_with_answer": [17, 18],
    },
    {
        "question": "How long is the quarantine period after returning from a planetary surface mission?",
        "expected": "14",
        "chunk_with_answer": [1, 7, 8, 11, 22, 23],
    },
    {
        "question": "How many gravitational sensors does the station use for dark matter mapping?",
        "expected": "24",
        "chunk_with_answer": [5, 21, 22, 23],
    },
    {
        "question": "How many hours of life support do emergency batteries provide during a power failure?",
        "expected": "72",
        "chunk_with_answer": [3, 15, 16],
    },
    # Unanswerable questions — the system should say it cannot answer
    {
        "question": "What is the annual budget of Starbase Omega?",
        "expected": "cannot",
        "chunk_with_answer": [],
    },
    {
        "question": "Who was the chief engineer before the current one?",
        "expected": "cannot",
        "chunk_with_answer": [],
    },
    {
        "question": "What is the maximum speed of the station's quantum drive?",
        "expected": "cannot",
        "chunk_with_answer": [],
    },
]
