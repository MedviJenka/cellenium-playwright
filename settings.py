from pathlib import Path
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parent
ENV_FILE = ROOT_DIR / ".env"


class __Config(BaseSettings):

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="allow")

    GOOGLE_SHEETS:        str  = Field(..., description='')
    GOOGLE_SHEET_API_KEY: str  = Field(..., description='')
    GOOGLE_SHEET_EMAIL:   str  = Field(..., description='')
    GOOGLE_SHEET_ID:      str  = Field(..., description='')
    OPENAI_MODEL:         str  = Field(..., description='')
    OPENAI_API_KEY:       str  = Field(..., description='')
    LOGFIRE_TOKEN:        str  = Field(..., description='')
    TEST_HEADLESS:        bool = Field(..., description='')
    CREDENTIALS_JSON:     Path = Field(..., description='google json credentials for accessing the sheet')

    @field_validator('CREDENTIALS_JSON')
    @classmethod
    def _resolve_from_root(cls, path: Path) -> Path:
        return path if path.is_absolute() else ROOT_DIR / path


Config = __Config()
