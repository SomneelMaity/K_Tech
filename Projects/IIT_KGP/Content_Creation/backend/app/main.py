import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# from .config import setting
# from .database import Base, engine


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = "*",
    allow_methods = "*",
    allow_headers = "*",
)

@app.get("/api/v1/health")
def health():
    return{
        "status": "Ok", "message": "Everything ok !!"
    }