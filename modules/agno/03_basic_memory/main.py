import os
from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

db = SqliteDb(db_file="basic_memory.db")

model = OpenAILike(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, id="gpt-4")
agent = Agent(
    model=model,
    name="Basic Agent Assistant",
    description="You are an expert in crafting story about japanesse anime",
    debug_mode=True,
    debug_level=2,
    db=db,
    user_id="user-1",
    enable_agentic_memory=True,
    instructions=(
        "You are an expert in crafting story about japanesse anime."
        "You will be given a prompt and you will respond with a short story."
        "The story should be engaging and entertaining."
        "The story should be in the style of a japanese anime."
        "The story should be 100 words long."
    ),
)

agent.print_response(
    {
        "role": "user",
        "content": "Craft a short story about a young girl who discovers she has the power to control the weather.",
    }
)
