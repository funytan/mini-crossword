import time
from typing import Optional

from loguru import logger
from numpy.random import choice

from src.models import ProcessedWord


def randomly_select(
    words: list[str], probabilities: Optional[list[float]] = None
) -> str:
    selected = choice(words, 1, p=probabilities)
    if isinstance(selected, ProcessedWord):
        return selected.variation
    else:
        return selected


def get_key(
    ch0: str = "*", ch1: str = "*", ch2: str = "*", ch3: str = "*", ch4: str = "*"
) -> str:
    return f"{ch0}{ch1}{ch2}{ch3}{ch4}"


def is_matchable(word: str) -> bool:
    vowels = ("a", "e", "i", "o", "u")
    if word[1] in vowels and word[3] in vowels:
        return True
    return False


def pprint(grid: list[list[str]]) -> None:
    for row in grid:
        print(row)
    print()


class Timer:
    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed_time = time.perf_counter() - self.start_time
        logger.info(f"{self.name} took {elapsed_time:.4f} seconds")
