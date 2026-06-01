from pydantic import BaseModel

class AddToWatchlistRequest(BaseModel):
    movie_id: int

class AddOrRemoveToWatchlistResponse(BaseModel):
    message: str

class GetFromWatchlistResponse(BaseModel):
    movie_ids: list[int]