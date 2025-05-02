from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings."""
    app_name: str = "Heart Failure Prediction API"
    model_path: str = "xgboost-model.pkl"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    """Get application settings."""
    return Settings()