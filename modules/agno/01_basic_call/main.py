import os
from agno.agent import Agent
from agno.models.openai import OpenAILike
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

model = OpenAILike(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, id="gpt-4")
agent = Agent(model=model, name="Basic Agent Assistant")

# response = agent.run("Hello, what's the meaning of life? answer in one word")
agent.print_response("Hello, what's the meaning of life? answer in one word")
