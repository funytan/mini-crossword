import asyncio

from src.config import AppSettings
from src.llm_utils import chat_completion_request_with_structured_output
from src.models import ClueAndHint, CluesAndHints, CrosswordSettings, Grid


async def generate_hints(
    grid: Grid, app_settings: AppSettings, crossword_settings: CrosswordSettings
) -> Grid | None:
    words = []

    for r in range(1, 6):
        word = "".join(grid.grid[r - 1])
        words.append((f"a{r}", word))

    for c in range(1, 6):
        word = "".join([grid.grid[r - 1][c - 1] for r in range(1, 6)])
        words.append((f"d{c}", word))

    messages_list = [
        {
            "role": "user",
            "content": ClUES_AND_HINTS_PROMPT.format(word=word.replace("_", "")),
        }
        for _, word in words
    ]

    tasks = [
        chat_completion_request_with_structured_output(
            client=app_settings.openai_client,
            messages=[msg],
            response_format=ClueAndHint,
        )
        for msg in messages_list
    ]

    results = await asyncio.gather(*tasks)

    grid.clues_and_hints = CluesAndHints(
        **(
            {f"clue_{label}": result.clue for (label, _), result in zip(words, results)}
            | {
                f"hint_{label}": result.hint
                for (label, _), result in zip(words, results)
            }
        )
    )

    return grid


ClUES_AND_HINTS_PROMPT = """\
You are a mini crossword puzzle creator.
Your task is to provide a clue for the word.
As far as possible, the clue should be concise and easy to understand, and should be tricky enough to make the user think.

Here is the word.:
{word}

Please provide the clue for the word. Only respond with the clue.
"""
