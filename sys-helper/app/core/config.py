from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OLLAMA_URL: str
    MODEL: str
    API_KEY: str
    MONGO_URL: str = "mongodb://localhost:27017"

    model_config = SettingsConfigDict(env_file=".env")
settings = Settings()