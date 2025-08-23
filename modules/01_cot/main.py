import json
from tools.broadcast import broadcast, broadcast_def
from tools.internet_search import internet_search, internet_search_def
from tools.research_aggregator import aggregate_research, aggregate_research_def
from tools.research_plan import research_plan, research_plan_def
from utils import openai_client

tools_defs = [
    research_plan_def,
    aggregate_research_def,
    internet_search_def,
    broadcast_def,
]
tools_dict = {
    "research_plan": research_plan,
    "aggregate_research": aggregate_research,
    "internet_search": internet_search,
    "broadcast": broadcast,
}


def execute_func(func_name: str, func_args: dict) -> str:
    func = tools_dict[func_name]
    if not func:
        return {
            "error": f"Function {func_name} not found.",
        }
    return func(**func_args)


def process_research(topic: str) -> None:
    SYSTEM_PROMPT = """
        You are a helpful research assistant.
        You will help me research a topic using the tools provided.

        # GUIDELINES
        1. Create the research plan for the topic.
        2. Do internet search for relevant information.
        3. Aggregate the information into a comprehensive summary.
        
        # IMPORTANT
        - You need to broadcast the progress of each step.
        - Broadcast message should be clear and concise.
        - Always use function calls to accomplish tasks.
        """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"Topic: {topic}.",
        },
    ]

    while True:
        res = openai_client.chat.completions.create(
            model="gpt-4o", messages=messages, tools=tools_defs, tool_choice="auto"
        )

        message = res.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)
                func_response = execute_func(func_name, func_args)
                messages.append(
                    {
                        "role": "tool",
                        "content": func_response,
                        "tool_call_id": tool_call.id,
                    }
                )
        else:
            break

    return "✅ Completed research for topic."


if __name__ == "__main__":
    input_topic = input("Enter the topic to research: ")
    print("---" * 10)
    process_research(input_topic)
