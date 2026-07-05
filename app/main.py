from fastapi import FastAPI

from app.config import settings
from app.routes import router

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    debug=settings.debug,
)


app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Welcome to CineAPI!"}
