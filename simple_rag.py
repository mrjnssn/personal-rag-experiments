import numpy as np

from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


document = Path("documents/notes.txt").read_text(encoding="utf-8")


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


response = client.embeddings.create(
    model="text-embedding-3-small",
    input=chunks
)

chunk_embedding = [
    item.embedding
    for item in response.data
]


question = input("What's your question? ")

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=question
)

question_embedding = response.data[0].embedding


def cosine_similarity(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)

    length_a = np.linalg.norm(vector_a)
    length_b = np.linalg.norm(vector_b)

    return dot_product / (length_a * length_b)


results = []

for index, chunk_embedding in enumerate(chunk_embedding):
    score = cosine_similarity(
        question_embedding,
        chunk_embedding
    )

    print(f"\n--- CHUNK {index} ---")
    print(f"Similarity: {score:.3f}")
    print(chunks[index])

    results.append({
        "chunk": chunks[index],
        "score": score
    })


results.sort(
    key=lambda result: result["score"],
    reverse=True
)

top_results = results[:3]

for result in top_results:
    print(f"\nScore: {result['score']:.3f}")
    print(result["chunk"])


context = "\n\n".join(
    result["chunk"]
    for result in top_results
)

prompt = f"""
answer the question based on the context below ONLY.

if the answer is not in the context, you say that you don't know the answer.

CONTEXT:
{context}

QUESTION:
{question}
"""

response = client.responses.create(
    model="gpt-5-nano",
    input=prompt
)

print("\nANSWER:")
print(response.output_text)






