from app.integrations.tmdb_client import TMDBClient
from app.services.movie_service import MovieService

def get_movie_service() -> MovieService:
    """Factory function to create a MovieService instance with its dependencies"""
    return MovieService(tmdb_client=TMDBClient())