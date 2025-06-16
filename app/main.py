from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.api.v1 import router as v1_router

app = FastAPI(
    title="AI Interview Assistant",
    description="Tech check via LLM",
    version="0.1.0",
)

app.include_router(v1_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
