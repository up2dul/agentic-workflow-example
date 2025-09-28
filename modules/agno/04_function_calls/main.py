import os
from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.tools.youtube import YouTubeTools
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

model = OpenAILike(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, id="gpt-4")
agent = Agent(
    model=model,
    name="YouTube Agent",
    description="You are a YouTube agent. Obtain the captions of a YouTube video and answer questions.",
    debug_mode=True,
    tools=[YouTubeTools()],
)

agent.print_response(
    {
        "role": "user",
        "content": "Summarize this video https://www.youtube.com/watch?v=Iv9dewmcFbs&t",
    },
    stream=True,
    markdown=True,
)
