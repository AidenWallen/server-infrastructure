from app.clients.ollama_client import OllamaClient
from app.prompts.engineer import SYSTEM_PROMPT
from app.core.logger import logger


async def process_chat(message: str, client: OllamaClient):
    logger.info(f"Processing chat message of length {len(message)}")
    try:
        response = await client.generate(
        prompt=message,
        system_prompt=SYSTEM_PROMPT
    )
        logger.info("Successfully generated response from Ollama")
        return response
    except Exception as e:
        logger.error(f"Error communicating with Ollama: {str(e)}")
        raise e
