from fastapi import FastAPI

app = FastAPI(title="Movie Streaming Platform", version="1.0")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health_check():
    return {"status": "ok"}