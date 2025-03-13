import random
from src.models import CrosswordSettings, Grid
from src.config import AppSettings
from src.loader import load
from loguru import logger
from src.utils import Timer, get_key
from src.crossword.word_picker import pick_a_3
from src.crossword.hint_generator import generate_hints


async def generate_crossword(
    app_settings: AppSettings, crossword_settings: CrosswordSettings
) -> Grid | None:
    with Timer("generate_crossword"):
        grid = Grid()
        grid = pick_a_3(grid, app_settings, crossword_settings)
    with Timer("generate_hints"):
        grid = await generate_hints(grid, app_settings, crossword_settings)
    return grid
