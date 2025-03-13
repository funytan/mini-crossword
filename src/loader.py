from collections import defaultdict
from itertools import product
from src.models import CrosswordSettings, ProcessedWord

from loguru import logger

from src.utils import is_matchable


def load_words(file_path: str) -> list[tuple[str, int]]:
    with open(file_path, "r") as f:
        words = [line.strip() for line in f][:-1]
    words = [(word, len(word)) for word in words if len(word) <= 5 and len(word) >= 3]
    logger.info(f"Loaded {len(words)} words")
    return words


def build_possible_word_variations(word: str, word_len: int) -> list[str]:
    if word_len == 3:
        return [f"__{word}", f"_{word}_", f"{word}__"]
    elif word_len == 4:
        return [
            f"{word}_",
            f"_{word}",
        ]
    elif word_len == 5:
        return [word]
    else:
        raise ValueError(f"invalid word lengt. Word is: {word}")


def build_preprocessed_words(words: list[tuple[str, int]]) -> list[ProcessedWord]:
    processed_words = []
    for word, word_len in words:
        possible_variations = build_possible_word_variations(word, word_len)
        for variation in possible_variations:
            processed_words.append(ProcessedWord(variation, word, word_len))

    logger.info(f"Created {len(processed_words)} variations from {len(words)} words.")
    return processed_words


def build_word_pattern_to_word_mapping(processed_words: list[ProcessedWord]) -> dict:
    characters = list("abcdefghijklmnopqrstuvwxyz*_")
    combinations = product(characters, repeat=5)
    word_pattern_to_word_mapping = {
        comb: set() for comb in ["".join(comb) for comb in combinations]
    }

    for tup in processed_words:
        variation, word, word_len = tup
        for item in product(
            ["*", variation[0]],
            ["*", variation[1]],
            ["*", variation[2]],
            ["*", variation[3]],
            ["*", variation[4]],
        ):
            word_pattern_to_word_mapping["".join(item)].add(variation)
    logger.info(
        f"Created word pattern to word mapping for {len(processed_words)} words."
    )
    return word_pattern_to_word_mapping


def build_matachable_words(processed_words: list[ProcessedWord]) -> list[str]:
    matchable_words = [
        processed_word.word
        for processed_word in processed_words
        if processed_word.length == 5 and is_matchable(processed_word.word)
    ]
    logger.info(f"Created {len(matchable_words)} matchable words.")
    return matchable_words


def load(file_path: str) -> tuple[dict, list[str]]:
    words = load_words(file_path)
    processed_words = build_preprocessed_words(words)
    word_pattern_to_word_mapping = build_word_pattern_to_word_mapping(processed_words)
    matchable_words = build_matachable_words(processed_words)
    return CrosswordSettings(
        matchable_words=matchable_words,
        word_pattern_to_word_mapping=word_pattern_to_word_mapping,
    )
