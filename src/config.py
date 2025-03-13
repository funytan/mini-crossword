from pydantic import Field
from pydantic_settings import BaseSettings
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


class AppSettings(BaseSettings):
    max_iterations: int = Field(
        alias="MAX_ITERATIONS", description="Maximum iterations"
    )
    openai_api_key: str = Field(alias="OPENAI_API_KEY", description="OpenAI API key")
    words_file_path: str = Field(
        alias="WORDS_FILE_PATH", description="Path to the words file"
    )

    @property
    def openai_client(self) -> AsyncOpenAI:
        return AsyncOpenAI(api_key=self.openai_api_key)

    class Config:
        env_file = ".env"


def get_app_settings() -> AppSettings:
    return AppSettings()
