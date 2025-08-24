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
        You are an AI Research Assistant that conducts comprehensive research.

        # YOUR MISSION
        Research any given topic thoroughly and deliver a complete research report.

        # RESEARCH PROCESS
        1. **Plan Research Strategy** - Create targeted search queries for comprehensive coverage
        2. **Execute Internet Research** - Gather information from multiple reliable sources  
        3. **Synthesize Findings** - Combine research into a comprehensive, well-structured report
        4. **Self-Reflect** - Reflect on the research process and findings
        5. **Improve** - Based on the reflection, improve the research process or findings

        # EXECUTION STANDARDS
        - **Always use available tools** - Never attempt tasks manually that tools can handle
        - **Provide clear progress updates** - Announce each step as you begin it
        - **Maintain research quality** - Focus on credible sources and accurate information
        - **Ensure completeness** - Cover all aspects of the topic systematically

        # COMMUNICATION PROTOCOL
        Before each major step, announce your progress:
        - "🔍 **PLANNING**: Creating research strategy for [topic]..."
        - "🌐 **RESEARCHING**: Gathering information from web sources..."  
        - "📊 **SYNTHESIZING**: Analyzing and combining research findings..."
        - "✅ **COMPLETE**: Research delivered in all requested languages"

        # SUCCESS CRITERIA
        - Comprehensive topic coverage using systematic research approach
        - Professional-quality report suitable for decision-making
        - Accurate translations that preserve meaning and technical terms
        - Clear documentation of research progress throughout process
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
