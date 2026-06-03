from pydantic import BaseModel

class MovieSummary(BaseModel):
    id: int
    title: str
    overview: str
    poster_path: str | None = None

class MovieListResponse(BaseModel):
    movies: list[MovieSummary]