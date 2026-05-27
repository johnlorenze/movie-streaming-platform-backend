import uvicorn

def main():
    print("Hello from movie-streaming-platform-backend!")
    uvicorn.run("app.main:app", reload=True)

if __name__ == "__main__":
    main()
