from lingualoop.conversations import build_messages
from lingualoop.llm import LLMClient


async def reply_to_message(user_message: str, llm: LLMClient) -> str:
    messages = build_messages(user_message)
    return await llm.chat(messages)