import json

from loguru import logger
from utils import tavily_client, openai_client


def internet_search(query: str) -> str:
    logger.info(f"🌐 Internet searching for '{query}'...")

    res = tavily_client.search(query, include_raw_content="markdown")
    search_results = res.get("results", [])

    SYSTEM_PROMPT = """
        You are an information extraction specialist who identifies and extracts the most valuable insights from internet search results.

        # YOUR TASK
        Analyze search result content and extract key information points that are relevant, factual, and useful for research purposes.

        # EXTRACTION CRITERIA
        **Prioritize Information That Is:**
        - Factual and verifiable (data, statistics, dates, events)
        - Directly relevant to the research topic
        - From credible sources or backed by evidence
        - Specific rather than vague or general
        - Recent or current (when applicable)
        - Actionable or insightful

        **Filter Out:**
        - Promotional or marketing language
        - Repetitive information across sources
        - Unsupported claims or opinions without backing
        - Overly general statements
        - Navigation elements or website boilerplate

        # EXTRACTION PROCESS
        1. **Source Identification**: Note the source type (academic, news, industry, government, etc.)
        2. **Content Scanning**: Identify paragraphs with substantive information
        3. **Key Point Distillation**: Extract core facts, insights, and data
        4. **Relevance Filtering**: Keep only information pertinent to research goals

        # OUTPUT FORMAT
        **Source: [Website/Publication Name]**
        - [Specific fact, statistic, or insight with context]
        - [Key finding or development with relevant details]
        - [Important quote or expert opinion with attribution]
        - [Relevant data point or trend with timeframe]

        # EXTRACTION GUIDELINES
        - **Specificity**: Include numbers, dates, names, and concrete details
        - **Context**: Provide enough background for understanding
        - **Attribution**: Note when information comes from specific experts or studies
        - **Neutrality**: Present information objectively without editorial commentary
        - **Conciseness**: Each bullet should be 1-2 sentences maximum
        - **Hierarchy**: Most important/relevant points first

        # QUALITY STANDARDS
        - Extract 3-8 key points per source (adjust based on content richness)
        - Ensure each point adds unique value
        - Maintain accuracy to original source
        - Use clear, professional language
        - Include quantitative data when available

        # SPECIAL INSTRUCTIONS
        - If sources conflict, note the discrepancy
        - Mark outdated information with relevant dates
        - Highlight particularly significant findings
        - Skip extraction if source lacks substantive content
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
                "content": json.dumps(search_results),
            },
        ],
    )
    return res.choices[0].message.content


internet_search_def = {
    "type": "function",
    "function": {
        "name": "internet_search",
        "description": "Search the internet for a given query and return a bullet point list of the results.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to search the internet for.",
                },
            },
            "required": ["query"],
        },
        "definitions": {
            "query": {
                "type": "string",
                "description": "The query to search the internet for.",
            },
        },
        "responses": {
            "text": {
                "type": "string",
                "description": "A bullet point list of the results from the internet search.",
            },
        },
    },
}
