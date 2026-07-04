from fastapi import FastAPI

from app.config import settings
from app.routes import router

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    debug=settings.DEBUG,
)


app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Welcome to CineAPI!"}
