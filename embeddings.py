from dotenv import load_dotenv
from openai import OpenAI

from config import EMBEDDING_MODEL


load_dotenv()
client = OpenAI()


def create_embedding(text):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding


def create_embeddings(texts):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )

    return [
        item.embedding
        for item in response.data
    ]

