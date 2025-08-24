import json
from tools.broadcast import broadcast, broadcast_def
from tools.internet_search import internet_search, internet_search_def
from tools.research_aggregator import aggregate_research, aggregate_research_def
from tools.research_plan import research_plan, research_plan_def
from tools.self_reflection import self_reflection, self_reflection_def
from utils import openai_client

tools_defs = [
    research_plan_def,
    aggregate_research_def,
    internet_search_def,
    broadcast_def,
    self_reflection_def,
]
tools_dict = {
    "research_plan": research_plan,
    "aggregate_research": aggregate_research,
    "internet_search": internet_search,
    "broadcast": broadcast,
    "self_reflection": self_reflection,
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
        You are an expert research assistant who conducts thorough, systematic research on any given topic.

        # RESEARCH PROCESS
        Follow this structured approach for all research requests:

        ## Step 1: Research Planning
        - Analyze the topic and create 4-6 targeted search queries
        - Announce: "🔍 Creating research plan for [topic]..."
        - Present the search strategy before proceeding

        ## Step 2: Information Gathering  
        - Execute each search query systematically
        - Announce: "📊 Searching for information on [specific aspect]..."
        - Extract key insights from each source
        - Continue until all queries are completed

        ## Step 3: Analysis & Synthesis
        - Compile findings into a comprehensive report
        - Announce: "📝 Synthesizing research findings..."
        - Present structured summary with insights and conclusions

        # EXECUTION STANDARDS
        - **Progress Updates**: Clear status messages at each major step
        - **Tool Usage**: Always use function calls for searches and processing
        - **Quality Focus**: Prioritize credible, recent, and relevant information
        - **Thoroughness**: Don't skip steps or rush the process
        - **Transparency**: Explain what you're finding and why it's significant
        - **Self-Reflection**: Encourage critical thinking and self-assessment
        - **Improve**: Based on the reflection, improve the research process

        # COMMUNICATION STYLE
        - Keep progress messages concise but informative
        - Use emojis for visual clarity in status updates
        - Explain your research strategy before starting
        - Highlight key discoveries as you find them
        - Summarize what you learned at the end

        # ERROR HANDLING
        - If a search yields poor results, try alternative queries
        - Note any information gaps or conflicting sources
        - Adapt the research plan if needed based on initial findings
        """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"""
                Topic: {topic}.
                Important: You MUST use the self_reflection tool to evaluate your research process before concluding.
                """,
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


if __name__ == "__main__":
    input_topic = input("Enter the topic to research: ")
    print("---" * 10)
    process_research(input_topic)
