from app.integrations.tmdb_client import TMDBClient
from app.schemas.movie import MovieSummary, MovieListResponse

class MovieService:
    def __init__(self, tmdb_client: TMDBClient):
        self.tmdb_client = tmdb_client

    async def get_trending_movies(self, page: int = 1) -> MovieListResponse:
        data = await self.tmdb_client.get_trending_movies(page)

        movies = [
            MovieSummary(
                id=movie["id"],
                title=movie["title"],
                overview=movie["overview"],
                poster_path=movie.get("poster_path")
            )
            for movie in data["results"]
        ]
        return MovieListResponse(movies=movies)

    # async def search_movies(self, query: str, page: int = 1) -> MovieListResponse:
    #     data = await self.tmdb_client.search_movies(query, page)
    #     movies = [
    #         {
    #             "id": movie["id"],
    #             "title": movie["title"],
    #             "overview": movie["overview"],
    #             "poster_path": movie.get("poster_path"),
    #         }      for movie in data.get("results", [])]
    #     return MovieListResponse(movies=movies)
    #
    # async def get_movie(self, movie_id: int):
    #     return await self.tmdb_client.get_movie(movie_id)
    #
    # async def get_recommendations(self, movie_id: int, page: int = 1):
    #     return await self.tmdb_client.get_recommendations(movie_id, page)
    #
    # async def get_videos(self, movie_id: int):
    #     return await self.tmdb_client.get_videos(movie_id)