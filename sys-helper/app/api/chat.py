from fastapi import APIRouter
from app.schemas.schemas import ChatRequest, ChatResponse
from app.services.chat_service import process_chat
from app.clients.ollama_client import OllamaClient, get_ollama_client
from fastapi import Depends

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    client: OllamaClient = Depends(get_ollama_client)
):
    response = await process_chat(request.message, client=client)

    return ChatResponse(
        response=response
    )