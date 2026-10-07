from functools import cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Relative paths resolve against the current working directory, i.e. the project using cellenium.
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    GOOGLE_SHEETS:        str         = Field(...,                       description='')
    OPENAI_MODEL:         str         = Field(...,                       description='')
    OPENAI_API_KEY:       str | None  = Field(None,                      description='')
    LOGFIRE_TOKEN:        str | None  = Field(None,                      description='')
    TEST_HEADLESS:        bool        = Field(True,                      description='')
    CREDENTIALS_JSON:     Path        = Field(Path("credentials.json"), description='google json credentials for accessing the sheet')


@cache
def get_config() -> Settings:
    """Load settings on first use so importing cellenium never requires a configured environment."""
    return Settings()
