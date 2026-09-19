from config import TOP_K, SIMILARITY_THRESHOLD
from embeddings import create_embedding
from llm import generate
from vector_store import get_collection


def retrieve(question):
    collection = get_collection()

    question_embedding = create_embedding(question)

    chroma_results = collection.query(
        query_embeddings=[question_embedding],
        n_results=TOP_K
    )

    results = []

    documents = chroma_results["documents"][0]
    metadatas = chroma_results["metadatas"][0]
    distances = chroma_results["distances"][0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):
        similarity = 1 - distance

        if similarity >= SIMILARITY_THRESHOLD:
            results.append({
                "filename": metadata["filename"],
                "chunk_id": metadata["chunk_id"],
                "text": document,
                "score": similarity
            })

    return results


def generate_answer(question, results):
    if not results:
        return "I have not found relevant information in the documents."

    context = "\n\n".join(
        f"Source: {result['filename']}\n{result['text']}"
        for result in results
    )

    prompt = f"""
    answer the question based on the context below ONLY.

    if the answer is not in the context, you say that you don't know the answer.

    CONTEXT:
    {context}

    QUESTION:
    {question}
    """

    return generate(prompt)
