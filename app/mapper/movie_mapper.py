from fastapi import HTTPException, status
from app.schemas.movie import MovieSummary, MovieListResponse

class MovieMapper:
    @staticmethod
    def to_summary(movie: dict) -> MovieSummary:
        try:
            return MovieSummary(
                id=movie["id"],
                title=movie["title"],
                overview=movie["overview"],
                poster_path=movie.get("poster_path")
            )
        except KeyError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid movie data structure from TMDB API"
            ) from e

    @classmethod
    def to_list_response(cls, data: dict) -> MovieListResponse:
        if "results" not in data:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid response from TMDB API"
            )

        return MovieListResponse(
            movies=[
                cls.to_summary(movie)
                for movie in data["results"]
            ]
        )
