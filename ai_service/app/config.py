from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LOG_ROOT_PATH: str = "logs"
    DATABASE_URL: str
    RABBITMQ_USER: str = "user"
    RABBITMQ_PASSWORD: str = "password"
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings() #type:ignore