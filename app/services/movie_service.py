from httpx import HTTPStatusError, RequestError
from fastapi import HTTPException, status
from app.integrations.tmdb_client import TMDBClient
from app.schemas.movie import MovieSummary, MovieListResponse, MovieTrailerResponse
from app.mapper.movie_mapper import MovieMapper

class MovieService:
    def __init__(self, tmdb_client: TMDBClient):
        self.tmdb_client = tmdb_client

    @staticmethod
    async def _execute_tmdb_request(func) -> dict:
        try:
            return await func()
        except HTTPStatusError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to fetch data from TMDB API"
            ) from e
        except RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="TMDB API is currently unavailable"
            ) from e
        except KeyError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Unexpected response structure from TMDB API"
            ) from e

    async def get_trending_movies(self, page: int = 1) -> MovieListResponse:
        trending_movies = await self._execute_tmdb_request(
            lambda: self.tmdb_client.get_trending_movies(page)
        )

        return MovieMapper.to_list_response(trending_movies)

    async def search_movies(self, query: str, page: int = 1) -> MovieListResponse:
        search_result = await self._execute_tmdb_request(
            lambda: self.tmdb_client.search_movies(query, page)
        )

        return MovieMapper.to_list_response(search_result)

    async def get_movie(self, movie_id: int) -> MovieSummary:
        movie = await self._execute_tmdb_request(
            lambda: self.tmdb_client.get_movie(movie_id)
        )

        if movie is None or "id" not in movie:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid response from TMDB API"
            )

        return MovieSummary(
            id=movie["id"],
            title=movie["title"],
            overview=movie["overview"],
            poster_path=movie.get("poster_path")
        )

    async def get_recommendations(self, movie_id: int, page: int = 1) -> MovieListResponse:
        recommendations = await self._execute_tmdb_request(
            lambda: self.tmdb_client.get_recommendations(movie_id, page)
        )

        return MovieMapper.to_list_response(recommendations)

    async def get_videos(self, movie_id: int) -> MovieTrailerResponse | None:
        videos = await self._execute_tmdb_request(
            lambda: self.tmdb_client.get_videos(movie_id)
        )

        if "results" not in videos:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid response from TMDB API"
            )

        trailer = next(
            (
                v
                for v in videos["results"]
                if v["site"] == "YouTube"
                and v["type"] == "Trailer"
            ),
            None,
        )

        return MovieTrailerResponse(youtube_key=trailer["key"]) if trailer else None