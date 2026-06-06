from pydantic import BaseModel, Field

class MovieSummary(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=1)
    overview: str = Field(min_length=1)
    poster_path: str | None = None

class MovieListResponse(BaseModel):
    movies: list[MovieSummary]

class MovieTrailerResponse(BaseModel):
    youtube_key: str = Field(min_length=1)