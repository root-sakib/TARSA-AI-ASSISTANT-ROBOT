from core.embeddings import embed, cosine

INTENTS = {
    "USER_SELF": [
        "who am i",
        "who i am",
        "do you know me",
        "my name",
        "tell me about myself"
    ],
    "ROBOT_ID": [
        "who are you",
        "what is your name"
    ]
}

# Precompute vectors
INTENT_VECTORS = {
    intent: [embed(q) for q in examples]
    for intent, examples in INTENTS.items()
}

def detect_intent_embedding(text: str, threshold=0.75):
    q_vec = embed(text)

    best_intent = None
    best_score = 0.0

    for intent, vecs in INTENT_VECTORS.items():
        for v in vecs:
            score = cosine(q_vec, v)
            if score > best_score:
                best_score = score
                best_intent = intent

    if best_score >= threshold:
        return best_intent, best_score

    return None, best_score
