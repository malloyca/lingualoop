import asyncio

from lingualoop.llm import LLMClient



async def main():
    client = LLMClient(
        base_url="http://localhost:1234/v1",
        model="qwen/qwen3.8-27b",
    )

    response = await client.chat([
        {
            "role": "user",
            "content": "Say hello in Mandarin Chinese.",
        }
    ])

    print(response)

if __name__ == "__main__":
    asyncio.run(main())