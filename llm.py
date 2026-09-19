from dotenv import load_dotenv
from openai import OpenAI

from config import LLM_MODEL


load_dotenv()

client = OpenAI()


def generate(prompt):
    response = client.responses.create(
        model=LLM_MODEL,
        input=prompt
    )

    return response.output_text