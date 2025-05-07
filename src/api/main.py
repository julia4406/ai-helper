from fastapi import FastAPI

app = FastAPI()

app.include_router(v1_router)