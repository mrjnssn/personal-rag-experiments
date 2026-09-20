# preparing documents for retrieval
import hashlib

from config import CHUNK_SIZE, EMBEDDING_PROVIDER, EMBEDDING_MODEL
from embeddings import create_embeddings
from documents import load_documents
from vector_store import get_collection, get_indexed_documents


def create_document_hash(text):
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()

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

    indexed_documents = get_indexed_documents()

    for document in documents:
        filename = document["filename"]
        text = document["text"]

        document_hash = create_document_hash(text)

        indexed_document = indexed_documents.get(filename)

        embedding_id = (
            f"{EMBEDDING_PROVIDER}:{EMBEDDING_MODEL}"
        )

        if not needs_reindexing(
            indexed_document,
            document_hash,
            embedding_id
        ):
            print(f"Unchanged: {filename}")
            continue
        
        collection.delete(
            where={"filename": filename}
        )

        chunks = create_chunks(text)
        embeddings = create_embeddings(chunks)

        ids = []
        metadatas = []

        for chunk_id, chunk in enumerate(chunks):
            ids.append(
                f"{filename}-{chunk_id}"
            )

            metadatas.append({
                "filename": filename,
                "chunk_id": chunk_id,
                "document_hash": document_hash,
                "embedding_id": embedding_id
            })

        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

        print(f"Indexed: {filename}")

    current_filenames = {
        document["filename"]
        for document in documents
    }

    for filename in indexed_documents:
        if filename not in current_filenames:
            collection.delete(
                where={"filename": filename}
            )

            print(f"Removed from index: {filename}")

    print(
        f"\nIndex was built. "
        f"{collection.count()} chunks in Chroma."
    )

def needs_reindexing(
    indexed_document,
    document_hash,
    embedding_id
):
    if not indexed_document:
        return True

    same_document = (
        indexed_document["document_hash"] == document_hash
    )

    same_embedding = (
        indexed_document["embedding_id"] == embedding_id
    )

    return not (
        same_document and same_embedding
    )



if __name__ == "__main__":
    build_index()