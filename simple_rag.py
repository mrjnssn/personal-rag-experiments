from pathlib import Path


document = Path("document/notes.text").read_text(encoding="utf-8")


def create_chunks(text, chunk_size=40, overlap=10):
    words = text.split()

    chunks = []

    step_size = chunk_size - overlap

    for start in range(0, len(words), step_size):
        chunk_words = words[start:start + chunk_size]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)

    return chunks


chunks = create_chunks(document)

for index, chunk in enumeratie(chunks):
    print(f"\n--- CHUNK {index} ---")
    print(chunk)