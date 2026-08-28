from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PlantationAI 360"
    app_version: str = "0.1.0"
    environment: str = "development"
    database_url: str = "sqlite:///./plantationai360.db"
    admin_api_token: str = "CHANGE-ME-PLANTATIONAI-ADMIN"
    cors_origins: str = "http://127.0.0.1:8780,http://localhost:8780"
    vision_disease_model: str = "models/vision/tea_disease/best.pt"
    crop_model: str = "models/crop/crop_forecast.joblib"
    crop_model_meta: str = "models/crop/crop_forecast.meta.json"
    nasa_power_base_url: str = "https://power.larc.nasa.gov/api/temporal/daily/point"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
