from fastapi import FastAPI

from config.logging import logger
from config.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.get("/")
def root():
    logger.info("Root endpoint accessed.")

    return {
        "message": f"Welcome to {settings.app_name}!",
        "version": settings.app_version,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }
