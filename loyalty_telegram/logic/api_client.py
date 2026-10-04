import httpx

from config import BACKEND_URL, API_REQUESTS

async def fast_test():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}{API_REQUESTS['test']}")
        return response.json()