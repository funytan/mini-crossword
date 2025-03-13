import random
from src.models import CrosswordSettings, Grid
from src.config import AppSettings
from src.loader import load
from loguru import logger
from src.utils import get_key


def pick_a_3(
    grid: Grid, app_settings: AppSettings, crossword_settings: CrosswordSettings
) -> Grid | None:
    candidate_words = crossword_settings.matchable_words
    random.shuffle(candidate_words)
    itr = 0
    while itr < app_settings.max_iterations:
        a_3 = candidate_words.pop()
        logger.info(f"{itr}, {a_3}")
        for idx, ch in enumerate(a_3):
            grid.grid[2][idx] = ch
        ans = pick_d_3(grid, app_settings, crossword_settings)
        if ans:
            return ans
        itr += 1
    return None


def pick_d_3(
    grid: Grid,
    app_settings: AppSettings,
    crossword_settings: CrosswordSettings,
    five_letters_only=True,
) -> Grid | None:
    middle_letter = grid.grid[2][2]
    possible_d_3 = [
        word for word in crossword_settings.matchable_words if word[2] == middle_letter
    ]
    if five_letters_only:
        candidate_words = [word for word in possible_d_3 if "_" not in word]
    else:
        candidate_words = possible_d_3
    random.shuffle(candidate_words)
    itr = 0
    while candidate_words and itr < app_settings.max_iterations:
        d_3 = candidate_words.pop()
        for idx, ch in enumerate(d_3):
            grid.grid[idx][2] = ch
        ans = pick_a_1(grid, app_settings, crossword_settings)
        if ans:
            return ans
        itr += 1
    return None


def pick_a_1(
    grid: Grid,
    app_settings: AppSettings,
    crossword_settings: CrosswordSettings,
    five_letters_only=True,
) -> Grid | None:
    middle_letter = grid.grid[0][2]
    possible_a_1 = crossword_settings.word_pattern_to_word_mapping[
        get_key(ch2=middle_letter)
    ]
    if five_letters_only:
        candidate_words = [word for word in possible_a_1 if "_" not in word]
    else:
        candidate_words = possible_a_1
    random.shuffle(candidate_words)
    itr = 0
    while candidate_words and itr < app_settings.max_iterations:
        a_1 = candidate_words.pop()
        for idx, ch in enumerate(a_1):
            grid.grid[0][idx] = ch
        ans = pick_a_2(grid, app_settings, crossword_settings)
        if ans:
            return ans
        itr += 1


def pick_a_2(
    grid: Grid,
    app_settings: AppSettings,
    crossword_settings: CrosswordSettings,
    five_letters_only=True,
) -> Grid | None:
    middle_letter = grid.grid[1][2]
    possible_a_2 = crossword_settings.word_pattern_to_word_mapping[
        get_key(ch2=middle_letter)
    ]
    if five_letters_only:
        candidate_words = [word for word in possible_a_2 if "_" not in word]
    else:
        candidate_words = possible_a_2
    random.shuffle(candidate_words)
    itr = 0
    while candidate_words and itr < app_settings.max_iterations:
        a_2 = candidate_words.pop()
        for idx, ch in enumerate(a_2):
            grid.grid[1][idx] = ch
        ans = pick_a_4(grid, app_settings, crossword_settings, five_letters_only=False)
        if ans:
            return ans
        itr += 1


def get_cands(word: str, crossword_settings: CrosswordSettings) -> list[str]:
    if len(word) == 4:
        return crossword_settings.word_pattern_to_word_mapping[
            get_key(ch0=word[0], ch1=word[1], ch2=word[2], ch3=word[3])
        ]
    elif len(word) == 5:
        return crossword_settings.word_pattern_to_word_mapping[
            get_key(ch0=word[0], ch1=word[1], ch2=word[2], ch3=word[3], ch4=word[4])
        ]
    else:
        raise ValueError(f"{word} has an unhandled length")


def verify_down(
    grid: Grid, down_len: int, crossword_settings: CrosswordSettings
) -> bool:
    d1 = ""
    for i in range(down_len):
        d1 += grid.grid[i][0]
    cand_d1 = get_cands(d1, crossword_settings)
    d2 = ""
    for i in range(down_len):
        d2 += grid.grid[i][1]
    cand_d2 = get_cands(d2, crossword_settings)
    d3 = ""
    for i in range(down_len):
        d3 += grid.grid[i][3]
    cand_d3 = get_cands(d3, crossword_settings)
    d4 = ""
    for i in range(down_len):
        d4 += grid.grid[i][4]
    cand_d4 = get_cands(d4, crossword_settings)
    if cand_d1 and cand_d2 and cand_d3 and cand_d4:
        return True
    return False


def pick_a_4(
    grid: Grid,
    app_settings: AppSettings,
    crossword_settings: CrosswordSettings,
    five_letters_only=False,
) -> Grid | None:
    middle_letter = grid.grid[3][2]
    possible_a_4 = crossword_settings.word_pattern_to_word_mapping[
        get_key(ch2=middle_letter)
    ]
    if five_letters_only:
        candidate_words = candidate_words = [
            word for word in possible_a_4 if "_" not in word
        ]
    else:
        candidate_words = list(possible_a_4)
    random.shuffle(candidate_words)
    itr = 0
    while candidate_words and itr < app_settings.max_iterations:
        a_4 = candidate_words.pop()
        for idx, ch in enumerate(a_4):
            grid.grid[3][idx] = ch
        if verify_down(grid, 4, crossword_settings):
            ans = pick_a_5(grid, app_settings, crossword_settings)
            if ans:
                return ans
        itr += 1


def pick_a_5(
    grid: Grid,
    app_settings: AppSettings,
    crossword_settings: CrosswordSettings,
    five_letters_only=False,
) -> Grid | None:
    middle_letter = grid.grid[4][2]
    possible_a_5 = crossword_settings.word_pattern_to_word_mapping[
        get_key(ch2=middle_letter)
    ]
    if five_letters_only:
        candidate_words = candidate_words = [
            word for word in possible_a_5 if "_" not in word
        ]
    else:
        candidate_words = list(possible_a_5)
    random.shuffle(candidate_words)
    itr = 0
    while candidate_words and itr < app_settings.max_iterations:
        a_5 = candidate_words.pop()
        for idx, ch in enumerate(a_5):
            grid.grid[4][idx] = ch
        if verify_down(grid, 5, crossword_settings):
            return grid
        itr += 1
