import os
import re
from openai import OpenAI
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

openai_client = OpenAI(base_url="https://api.unli.dev/v1")
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text
