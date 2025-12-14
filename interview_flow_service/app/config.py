from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str
    RABBITMQ_USER: str = "user"
    RABBITMQ_PASSWORD: str = "password"
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    MAX_INTRO_QUESTIONS: int = 1
    MAX_PROJ_AND_INTERVIEW_QUESTIONS: int = 5

    class Config:
        env_file = ".env"

settings = Settings() #type:ignore