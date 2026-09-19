# preparing documents for retrieval

import json
from pathlib import Path

from config import (
    EMBEDDINGS_FILE,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

from embeddings import create_embeddings
from documents import load_documents


def create_chunks(text):
    words = text.split()
    chunks = []

    step_size = CHUNK_SIZE - CHUNK_OVERLAP

    for start in range(0, len(words), step_size):
        chunk_words = words[start:start + CHUNK_SIZE]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)

    return chunks


def build_index():
    documents = load_documents()

    records = []

    for document in documents:
        chunks = create_chunks(document["text"])

        embeddings = create_embeddings(chunks)

        for chunk, embedding in zip(chunks, embeddings):
            records.append({
                "filename": document["filename"],
                "text": chunk,
                "embedding": embedding
            })

    output_path = Path(EMBEDDINGS_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(records, file)
    
    print(f"{len(records)} chunks have been indexed.")


if __name__ == "__main__":
    build_index()