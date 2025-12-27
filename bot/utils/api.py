import aiohttp
from ..config import BACKEND_URL

class APIClient:
    def __init__(self):
        self.base_url = f"{BACKEND_URL}/api/"

    async def create_media(self, data: dict):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}movie/", json=data) as response:
                return await response.json()

    async def get_media_by_code(self, code: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}movie_code/{code}") as response:
                if response.status == 200:
                    return await response.json()
                return None

    async def get_media_by_id(self, media_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}movie/{media_id}/") as response:
                if response.status == 200:
                    return await response.json()
                return None

    async def get_episode(self, episode_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}episodes/{episode_id}/") as response:
                if response.status == 200:
                    return await response.json()
                return None

api_client = APIClient()
