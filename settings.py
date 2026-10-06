from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parent / ".env"


class __Config(BaseSettings):

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    GOOGLE_SHEETS:        str = Field(..., description='')
    GOOGLE_SHEET_API_KEY: str = Field(..., description='')
    GOOGLE_SHEET_EMAIL:   str = Field(..., description='')
    GOOGLE_SHEET_ID:      str = Field(..., description='')
    OPENAI_MODEL:         str = Field(..., description='')
    LOGFIRE_TOKEN:        str = Field(..., description='')


Config = __Config()
