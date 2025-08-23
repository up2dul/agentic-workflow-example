from loguru import logger
from utils import openai_client


def research_plan(topic: str) -> str:
    logger.info(f"📝 Generating research plan for '{topic}'...")

    SYSTEM_PROMPT = """
        You are a research strategy expert who creates comprehensive search plans for any given topic.

        # YOUR TASK
        Analyze the research topic and generate a strategic list of search queries that will provide thorough coverage of the subject from multiple angles.

        # QUERY DESIGN PRINCIPLES
        - **Specificity**: Each query should target distinct aspects or subtopics
        - **Diversity**: Cover different perspectives (academic, industry, recent developments, case studies)
        - **Searchability**: Use terms and phrases likely to appear in relevant sources
        - **Complementary**: Queries should build upon each other without significant overlap

        # OUTPUT REQUIREMENTS
        - Generate 4-6 search queries
        - Each query should be 3-8 words for optimal search engine performance
        - Include a brief rationale (1 sentence) explaining what each query targets
        - Arrange queries in logical research order (foundational → specific → current)

        # QUERY TYPES TO CONSIDER
        - Foundational/definitional queries
        - Current trends and recent developments
        - Expert opinions and analysis
        - Case studies or real-world applications
        - Comparative or alternative perspectives
        - Statistical data and research findings
        """

    res = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"Create a research plan for {topic}.",
            },
        ],
    )
    return res.choices[0].message.content


research_plan_def = {
    "type": "function",
    "function": {
        "name": "research_plan",
        "description": "Generate a research plan for a given topic.",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The topic to generate a research plan for.",
                },
            },
            "required": ["topic"],
        },
        "definitions": {
            "topic": {
                "type": "string",
                "description": "The topic to generate a research plan for.",
            },
        },
        "responses": {
            "text": {
                "type": "string",
                "description": "The research plan for the given topic.",
            },
        },
    },
}
