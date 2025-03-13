from typing import List, Dict, Annotated, Optional
from pydantic import BaseModel, Field
from openai import OpenAI
from collections import namedtuple, defaultdict

ProcessedWord = namedtuple("ProcessedWord", ["variation", "word", "length"])


class CrosswordSettings(BaseModel):
    matchable_words: List[str] = Field(description="List of matchable words")
    word_pattern_to_word_mapping: Dict[str, set] = Field(
        default_factory=lambda: defaultdict(set),
        description="Mapping of word pattern to word",
    )


class Grid(BaseModel, validate_assignment=True):
    grid: List[List[str]] = Field(
        default_factory=lambda: [["." for _ in range(5)] for _ in range(5)]
    )
    clues_and_hints: Optional["CluesAndHints"] = None


class CluesAndHints(BaseModel):
    clue_a1: Annotated[Optional[str], Field(description="Clue for A1")] = None
    clue_a2: Annotated[Optional[str], Field(description="Clue for A2")] = None
    clue_a3: Annotated[Optional[str], Field(description="Clue for A3")] = None
    clue_a4: Annotated[Optional[str], Field(description="Clue for A4")] = None
    clue_a5: Annotated[Optional[str], Field(description="Clue for A5")] = None
    clue_d1: Annotated[Optional[str], Field(description="Clue for D1")] = None
    clue_d2: Annotated[Optional[str], Field(description="Clue for D2")] = None
    clue_d3: Annotated[Optional[str], Field(description="Clue for D3")] = None
    clue_d4: Annotated[Optional[str], Field(description="Clue for D4")] = None
    clue_d5: Annotated[Optional[str], Field(description="Clue for D5")] = None
    hint_a1: Annotated[Optional[str], Field(description="Hint for A1")] = None
    hint_a2: Annotated[Optional[str], Field(description="Hint for A2")] = None
    hint_a3: Annotated[Optional[str], Field(description="Hint for A3")] = None
    hint_a4: Annotated[Optional[str], Field(description="Hint for A4")] = None
    hint_a5: Annotated[Optional[str], Field(description="Hint for A5")] = None
    hint_d1: Annotated[Optional[str], Field(description="Hint for D1")] = None
    hint_d2: Annotated[Optional[str], Field(description="Hint for D2")] = None
    hint_d3: Annotated[Optional[str], Field(description="Hint for D3")] = None
    hint_d4: Annotated[Optional[str], Field(description="Hint for D4")] = None
    hint_d5: Annotated[Optional[str], Field(description="Hint for D5")] = None


class ClueAndHint(BaseModel):
    clue: str = Field(
        description="Clue for the word, this will be first shown to the user."
    )
    hint: str = Field(
        description="Hint for the word, this will be shown if the user asks for a further hint. The hint should build on the clue and make it easier for the user to guess the word."
    )
