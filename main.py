from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from mangum import Mangum

from src.config import AppSettings, get_app_settings
from src.crossword.crossword_builder import generate_crossword
from src.loader import load
from src.models import Grid


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Preload resources
        logger.info("Loading application settings...")
        app.state.app_settings = get_app_settings()
        logger.info("Loading crossword settings...")
        app.state.crossword_settings = load(app.state.app_settings.words_file_path)
        logger.info("Settings loaded successfully.")
        yield
    except Exception as e:
        logger.error(f"Error during application startup: {e}")
        raise e


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

handler = Mangum(app)


def get_app_settings_dep() -> AppSettings:
    return app.state.app_settings


def get_crossword_settings_dep():
    return app.state.crossword_settings


@app.get("/generate")
async def predict(
    app_settings: AppSettings = Depends(get_app_settings_dep),
    crossword_settings=Depends(get_crossword_settings_dep),
) -> Grid | None:
    return await generate_crossword(app_settings, crossword_settings)
