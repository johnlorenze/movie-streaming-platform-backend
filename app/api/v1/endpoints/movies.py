from fastapi import APIRouter, Depends
from app.services.movie_service import MovieService
from app.schemas.movie import MovieListResponse
from app.dependencies.services import get_movie_service

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get(
    "/trending",
    summary="Get Trending Movies",
    description="Fetches a list of trending movies for the week.",
    response_model=MovieListResponse
)
async def get_trending_movies(
        page: int = 1,
        movie_service: MovieService = Depends(get_movie_service)
) -> MovieListResponse:
    return await movie_service.get_trending_movies(page)