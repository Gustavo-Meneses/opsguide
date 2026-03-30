import os

def load_knowledge_base(path="data/base_conhecimento.txt"):
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # separa por blocos
    chunks = content.split("\n\n")
    return [c.strip() for c in chunks if c.strip()]


def simple_similarity_search(query, knowledge_base, top_k=3):
    query_words = set(query.lower().split())

    scored = []

    for chunk in knowledge_base:
        chunk_words = set(chunk.lower().split())
        score = len(query_words & chunk_words)
        scored.append((score, chunk))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [chunk for score, chunk in scored[:top_k] if score > 0]
