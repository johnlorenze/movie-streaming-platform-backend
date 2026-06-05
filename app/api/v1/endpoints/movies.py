from fastapi import APIRouter, Depends
from app.services.movie_service import MovieService
from app.schemas.movie import MovieListResponse, MovieSummary, MovieTrailerResponse
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

@router.get(
    "/search",
    summary="Search Movies",
    description="Searches for movies based on a query string.",
    response_model=MovieListResponse
)
async def search_movies(
    q: str,
    page: int = 1,
    movie_service: MovieService = Depends(get_movie_service)
) -> MovieListResponse:
    return await movie_service.search_movies(q, page)

@router.get(
    "/{movie_id}",
    summary="Get Movie Details",
    description="Fetches detailed information about a specific movie.",
    response_model=MovieSummary
)
async def get_movie_details(
    movie_id: int,
    movie_service: MovieService = Depends(get_movie_service)
) -> MovieSummary:
    return await movie_service.get_movie(movie_id)

@router.get(
    "/{movie_id}/recommendations",
    summary="Get Movie Recommendations",
    description="Fetches a list of recommended movies based on a specific movie.",
    response_model=MovieListResponse
)
async def get_movie_recommendations(
    movie_id: int,
    page: int = 1,
    movie_service: MovieService = Depends(get_movie_service)
) -> MovieListResponse:
    return await movie_service.get_recommendations(movie_id, page)

@router.get(
    "/{movie_id}/trailer",
    summary="Get Movie Trailer",
    description="Fetches the YouTube key for the trailer of a specific movie.",
    response_model=MovieTrailerResponse | None
)
async def get_movie_trailer(
    movie_id: int,
    movie_service: MovieService = Depends(get_movie_service)
) -> MovieTrailerResponse | None:
    return await movie_service.get_videos(movie_id)