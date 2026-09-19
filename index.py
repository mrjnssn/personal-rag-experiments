# preparing documents for retrieval

from config import CHUNK_SIZE
from embeddings import create_embeddings
from documents import load_documents
from vector_store import get_collection


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
    collection = get_collection()

    for document in documents:
        chunks = create_chunks(document["text"])
        embeddings = create_embeddings(chunks)

        ids = []
        metadatas = []

        for chunk_id, chunk in enumerate(chunks):
            ids.append(
                f"{document['filename']}-{chunk_id}"
            )

            metadatas.append({
                "filename": document["filename"],
                "chunk_id": chunk_id
            })

        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

    print(
        f"Index was built. "
        f"{collection.count()} chunks in Chroma."
    )
    

if __name__ == "__main__":
    build_index()