import asyncio

from lingualoop.llm import LLMClient



async def main():
    client = LLMClient(
        base_url="http://localhost:1234/v1",
        model="qwen/qwen3.8-27b",
    )

    try:
        response = await client.chat([
            {
                "role": "user",
                "content": "Say 'Hello.' in Mandarin Chinese.",
            }
        ])
        print(response)
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
