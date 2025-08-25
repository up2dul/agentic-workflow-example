from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

load_dotenv()


@function_tool("get_weather")
def get_weather(location: str) -> dict[str, str]:
    """Get the current weather for a given location."""
    return {
        "location": location,
        "temperature": "25°C",
        "humidity": "60%",
    }


@function_tool("get_trending_animes")
def get_trending_animes() -> list[dict[str, any]]:
    """Get the current trending anime titles and ratings."""
    return [
        {"title": "Kimetsu no Yaiba: Infinity Castle", "rating": 8.8, type: "Movie"},
        {"title": "Dr. Stone 4th Season", "rating": 8.5, "type": "Series"},
        {"title": "Sakamoto Days", "rating": 7.8, "type": "Series"},
    ]


weather_agent = Agent(
    name="Weather Agent",
    instructions="You are a weather agent. You will provide the weather for a given location.",
    model="gpt-4.1",
    tools=[get_weather],
)

trending_anime_agent = Agent(
    name="Trending Anime Agent",
    instructions="You are a trending anime agent. You will provide the trending anime titles and ratings.",
    model="gpt-4.1",
    tools=[get_trending_animes],
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="""
        You are a Triage Agent that routes conversations to specialized agents based on user queries.

        # ROUTING RULES:
        - Weather queries → Hand off to Weather Agent
        - Anime/trending anime queries → Hand off to Trending Anime Agent  
        - All other queries → Handle directly

        # EXAMPLES:
        - "What's the weather like?" → Weather Agent
        - "Current trending anime?" → Trending Anime Agent
        - "How are you?" → Handle yourself

        Be decisive and route quickly based on the main topic of the user's question.
        """,
    model="gpt-4.1",
    handoffs=[
        weather_agent,
        trending_anime_agent,
    ],
)


async def run_agent() -> None:
    messages = []

    while True:
        print("---" * 20)
        print("Type 'exit' to exit the program.")
        user_input = input("You: ")
        if user_input.strip() == "exit":
            break
        print("===" * 10)

        messages.append({"role": "user", "content": user_input})
        runner = await Runner.run(starting_agent=triage_agent, input=messages)
        messages = runner.to_input_list()

        print(f"Agent: {runner.last_agent.name}")
        print(runner.final_output)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_agent())
