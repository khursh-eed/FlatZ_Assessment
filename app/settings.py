from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./flatz.db"
    openai_api_key: str = ""
    openai_api_url: str = "https://api.openai.com/v1/chat/completions"
    model: str = "gpt-3.5-turbo"
    ai_provider: str = "openai"  # hf (not implemented here)

    # sub class to check for env files
    class Config:
        env_file = ".env"

settings = Settings()