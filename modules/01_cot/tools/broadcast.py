from loguru import logger


def broadcast(message: str) -> None:
    logger.info(message)


broadcast_def = {
    "type": "function",
    "function": {
        "name": "broadcast",
        "description": "Broadcast a message to all tools.",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message to broadcast.",
                },
            },
            "required": ["message"],
        },
        "definitions": {
            "message": {
                "type": "string",
                "description": "The message to broadcast.",
            },
        },
    },
}
