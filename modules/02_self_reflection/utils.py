import os
import re

from dotenv import load_dotenv
from tavily import TavilyClient
from langfuse.openai import openai

load_dotenv()

openai_client = openai
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text
