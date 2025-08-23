from loguru import logger
from utils import openai_client, slugify


def aggregate_research(topic: str, content: str) -> str:
    logger.info(f"✍️ Aggregating research for '{topic}'...")

    SYSTEM_PROMPT = """
        You are a research synthesis expert who transforms raw research data into comprehensive, actionable reports.

        # YOUR TASK
        Analyze multiple research sources and synthesize them into a cohesive, well-structured report that provides clear insights and actionable understanding of the topic.

        # ANALYSIS REQUIREMENTS
        - **Source Integration**: Weave information from multiple sources into unified insights
        - **Pattern Recognition**: Identify common themes, contradictions, and knowledge gaps
        - **Critical Evaluation**: Assess source reliability and note conflicting information
        - **Contextual Relevance**: Prioritize information based on recency, authority, and relevance

        # REPORT STRUCTURE
        ## Executive Summary (2-3 paragraphs)
        - Key findings and main conclusions
        - Most important insights for quick understanding

        ## Core Findings
        - **Definition & Context**: Clear explanation of the topic and its significance
        - **Current State**: Present situation, trends, and recent developments  
        - **Key Players/Stakeholders**: Important organizations, experts, or entities involved
        - **Challenges & Opportunities**: Main obstacles and potential areas for growth

        ## Detailed Analysis
        - **Supporting Evidence**: Data, statistics, and concrete examples
        - **Multiple Perspectives**: Different viewpoints and approaches
        - **Case Studies**: Real-world applications or examples (if applicable)

        ## Implications & Future Outlook
        - **Trends & Predictions**: Where the field/topic is heading
        - **Recommendations**: Actionable insights for different stakeholders
        - **Areas for Further Research**: Identified knowledge gaps

        ## Sources & Reliability Assessment
        - Brief evaluation of source quality and potential biases
        - Note any conflicting information or uncertainty

        # WRITING STANDARDS
        - Use clear, professional language accessible to educated non-experts
        - Support claims with specific evidence and examples
        - Maintain objective tone while highlighting significant insights
        - Include relevant statistics, dates, and concrete details
        - Ensure logical flow between sections

        # QUALITY INDICATORS
        - Synthesis (not just summary) of information
        - Clear distinction between established facts and emerging trends
        - Balanced presentation of different viewpoints
        - Actionable insights and practical implications
        - Proper context and significance of findings

        Length: 1000-2000 words depending on topic complexity and source richness.
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
                "content": f"Topic: {topic}\nContent after research: {content}",
            },
        ],
    )

    result_file_name = slugify(topic)
    with open(f"results/{result_file_name}.md", "w") as file:
        file.write(res.choices[0].message.content)

    return f"Research plan for {topic} has been aggregated and saved to {topic}.md."


aggregate_research_def = {
    "type": "function",
    "function": {
        "name": "aggregate_research",
        "description": "Generate a comprehensive and detailed summary of a given topic and content.",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The topic to generate a summary for.",
                },
                "content": {
                    "type": "string",
                    "description": "The content to generate a summary for.",
                },
            },
            "required": ["topic", "content"],
        },
        "definitions": {
            "topic": {
                "type": "string",
                "description": "The topic to generate a summary for.",
            },
            "content": {
                "type": "string",
                "description": "The content to generate a summary for.",
            },
        },
        "responses": {
            "text": {
                "type": "string",
                "description": "The summary of the given topic and content.",
            },
        },
    },
}
