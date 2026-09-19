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