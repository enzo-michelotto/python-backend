from pydantic_settings import BaseSettings


class Settings(BaseSettings):  # type: ignore
    DATABASE_URL: str
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
