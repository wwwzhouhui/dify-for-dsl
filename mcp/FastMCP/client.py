import asyncio
from fastmcp import Client

async def example():
    async with Client("http://127.0.0.1:8002/mcp") as client:
        await client.ping()

if __name__ == "__main__":
    asyncio.run(example())