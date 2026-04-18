EVAL_DATASET = [
    {
        "question": "How many crew members does Starbase Omega have?",
        "expected": "312",
    },
    {
        "question": "What is the water recycling efficiency rate on the station?",
        "expected": "97.3%",
    },
    {
        "question": "How long is the quarantine period after returning from a planetary surface mission?",
        "expected": "14",
    },
    {
        "question": "How many gravitational sensors does the station use for dark matter mapping?",
        "expected": "24",
    },
    {
        "question": "How many hours of life support do emergency batteries provide during a power failure?",
        "expected": "72",
    },
    # Unanswerable questions — the system should say it cannot answer
    {
        "question": "What is the annual budget of Starbase Omega?",
        "expected": "cannot",
    },
    {
        "question": "Who was the chief engineer before the current one?",
        "expected": "cannot",
    },
    {
        "question": "What is the maximum speed of the station's quantum drive?",
        "expected": "cannot",
    },
]
