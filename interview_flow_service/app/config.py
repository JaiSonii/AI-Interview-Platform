from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    JOB_SERVICE_URL: str
    MAX_INTRO_QUESTIONS: int = 1
    MAX_PROJ_AND_INTERVIEW_QUESTIONS: int = 5

    class Config:
        env_file = ".env"

settings = Settings() #type:ignore