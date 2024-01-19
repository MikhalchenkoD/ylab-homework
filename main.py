import uvicorn
from fastapi import FastAPI
import routes

app = FastAPI()

BASE_API_URL = "/api/v1/"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
