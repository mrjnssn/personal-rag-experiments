from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5-nano",
    input="leg in 1 zin uit wat RAG is"
)