from fastapi import APIRouter, Request

from lingualoop.schemas import ChatRequest, ChatResponse
from lingualoop.services.chat import reply_to_message


router = APIRouter()


@router.post("/api/chat")
async def chat(
    request: ChatRequest,
    http_request: Request,
) -> ChatResponse:
    llm = http_request.app.state.llm

    response = await reply_to_message(request.message, llm)

    return ChatResponse(response=response)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "database": "ready"}
