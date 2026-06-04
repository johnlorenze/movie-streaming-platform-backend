import httpx
from app.core.config import settings

class TMDBClient:
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.base_url = settings.TMDB_BASE_URL

    async def _get(self, endpoint: str, params: dict | None = None):
        params = params or {}
        params['api_key'] = self.api_key

        url = f"{self.base_url}{endpoint}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

            return response.json()

    async def get_trending_movies(self, page: int = 1):
        return await self._get("/trending/movie/week", {"page": page})

    async def search_movies(self, query: str, page: int = 1):
        return await self._get("/search/movie", {"query": query, "page": page})

    async def get_movie(self, movie_id: int):
        return await self._get(f"/movie/{movie_id}")

    async def get_recommendations(self, movie_id: int, page: int = 1):
        return await self._get(f"/movie/{movie_id}/recommendations", {"page": page})

    async def get_videos(self, movie_id: int):
        return await self._get(f"/movie/{movie_id}/videos")