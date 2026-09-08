from lingualoop.llm import Message



def build_messages(user_message: str) -> list[Message]:
    return [
        {
            "role": "user",
            "content": user_message,
        }
    ]