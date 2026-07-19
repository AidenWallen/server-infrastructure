import httpx
from app.core.config import settings

class OllamaClient:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model

    async def generate(self, prompt: str, system_prompt: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                    self.base_url,
                json={
                        "model": self.model,
                    "system": system_prompt,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )
            response.raise_for_status()
            return response.json()["response"]

def get_ollama_client():
    return OllamaClient(base_url=settings.OLLAMA_URL, model=settings.MODEL)
