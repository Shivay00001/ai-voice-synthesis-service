from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Voice Synthesis Service"
    API_V1_STR: str = "/api/v1"
    
    # TTS Settings
    DEFAULT_MODEL_NAME: str = "tts_models/en/ljspeech/vits"
    USE_GPU: bool = False
    
    # Storage
    OUTPUT_FOLDER: str = "output"
    
    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
