import chromadb

from config import CHROMA_PATH, COLLECTION_NAME


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

def get_collection():
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        configuration={
            "hnsw": {
                "space": "cosine"
            }
        }
    )

def get_indexed_documents():
    collection = get_collection()

    results = collection.get(
        include=["metadatas"]
    )

    indexed_documents = {}

    for metadata in results["metadatas"]:
        filename = metadata["filename"]
        document_hash = metadata["document_hash"]

        indexed_documents[filename] = document_hash
    
    return indexed_documents