from src.config import AppSettings
from src.crossword.hint_generator import generate_hints
from src.crossword.word_picker import pick_a_3
from src.models import CrosswordSettings, Grid
from src.utils import Timer


async def generate_crossword(
    app_settings: AppSettings, crossword_settings: CrosswordSettings
) -> Grid | None:
    with Timer("generate_crossword"):
        grid = Grid()
        grid = pick_a_3(grid, app_settings, crossword_settings)
    with Timer("generate_hints"):
        grid = await generate_hints(grid, app_settings, crossword_settings)
    return grid
