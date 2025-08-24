from loguru import logger
from utils import openai_client


def self_reflection(query: str, result: str) -> str | None:
    logger.info(f"💭 Self-reflection: {query}")

    SYSTEM_PROMPT = """
        You are a professional research quality evaluator and expert reviewer.
        Your task is to provide a comprehensive self-reflection on the given research query and results.

        # Evaluation Criteria
        1. **Completeness**: Does the research cover all important aspects?
        2. **Accuracy**: Is the information reliable and well-sourced?
        3. **Depth**: Is the analysis thorough and insightful?
        4. **Structure**: Is the research well-organized and logical?
        5. **Relevance**: Does it directly address the research topic?

        # Output Format
        **RESEARCH QUALITY ASSESSMENT**
        
        **Overall Score**: [X/10]
        
        **Strengths**:
        - [List key strengths]
        
        **Areas for Improvement**:
        - [Specific improvements needed]
        
        **Missing Elements**:
        - [What's missing or could be added]
        
        **Recommendation**:
        - [Overall assessment and next steps]
        """

    res = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Query: {query}\nResult: {result}"},
        ],
    )

    return res.choices[0].message.content


self_reflection_def = {
    "type": "function",
    "function": {
        "name": "self_reflection",
        "description": "Reflect on the given query and result and provide a self-reflection.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query that was used to generate the result.",
                },
                "result": {
                    "type": "string",
                    "description": "The result that was generated.",
                },
            },
            "required": ["query", "result"],
        },
        "definitions": {
            "query": {
                "type": "string",
                "description": "The query that was used to generate the result.",
            },
            "result": {
                "type": "string",
                "description": "The result that was generated.",
            },
        },
    },
}
