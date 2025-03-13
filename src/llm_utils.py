from typing import Optional, Type

from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential
from pydantic import BaseModel


@retry(
    wait=wait_random_exponential(multiplier=1, max=4),
    stop=stop_after_attempt(5),
)
async def chat_completion_request(
    client: AsyncOpenAI,
    messages: list[dict[str, str]],
    model: Optional[str] = "gpt-4o-2024-08-06",
    temperature: Optional[float] = 0,
) -> str:
    request_body = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    try:
        response = await client.chat.completions.create(**request_body)
    except Exception as e:
        raise
    return response.choices[0].message.content


@retry(
    wait=wait_random_exponential(multiplier=1, max=4),
    stop=stop_after_attempt(5),
)
async def chat_completion_request_with_structured_output(
    client: AsyncOpenAI,
    messages: list[dict[str, str]],
    response_format: Type[BaseModel],
    model: Optional[str] = "gpt-4o-2024-08-06",
    temperature: Optional[float] = 0,
) -> BaseModel:
    completion = await client.beta.chat.completions.parse(
        model=model,
        messages=messages,
        response_format=response_format,
        temperature=temperature,
    )

    return completion.choices[0].message.parsed
