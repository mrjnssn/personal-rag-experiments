import json

import numpy as np

from config import EMBEDDINGS_FILE, TOP_K
from embeddings import create_embedding
from llm import generate


def cosine_similarity(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)

    length_a = np.linalg.norm(vector_a)
    length_b = np.linalg.norm(vector_b)

    return dot_product / (length_a * length_b)


def load_index():
    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def retrieve(question):
    data = load_index()

    question_embedding = create_embedding(question)

    results = []

    for item in data:
        score = cosine_similarity(
            question_embedding,
            item["embedding"]
        )

        results.append({
            "filename": item["filename"],
            "text": item["text"],
            "score": score
        })

    results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    return results[:TOP_K]


def generate_answer(question, results):
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
