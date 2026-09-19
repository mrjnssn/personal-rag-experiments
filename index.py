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
    paragraphs = text.split("\n\n")
    
    chunks = []
    current_chunk = []

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        current_text = " ".join(current_chunk)
        current_words = len(current_text.split())
        paragraph_words = len(paragraph.split())

        if current_words + paragraph_words <= CHUNK_SIZE:
            current_chunk.append(paragraph)

        else:
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))

            current_chunk = [paragraph]

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks


def build_index():
    documents = load_documents()

    records = []

    for document in documents:
        chunks = create_chunks(document["text"])

        for chunk_id, chunk in enumerate(chunks):
            print(f"\n--- {document['filename']} | chunk {chunk_id} ---")
            print(chunk)

        embeddings = create_embeddings(chunks)

        for chunk_id, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            records.append({
                "filename": document["filename"],
                "chunk_id": chunk_id,
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