"""Configuration module using Pydantic Settings"""

from enum import Enum
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotMode(str, Enum):
    """Bot running mode"""

    POLLING = "polling"
    WEBHOOK = "webhook"


class Settings(BaseSettings):
    """Application settings"""

    # Bot settings
    bot_token: str = Field(..., description="Telegram Bot API Token")
    bot_mode: BotMode = Field(
        default=BotMode.POLLING, description="Bot mode: polling or webhook"
    )

    # Webhook settings (for production)
    webhook_url: str = Field(default="", description="Webhook URL for production mode")
    webhook_path: str = Field(default="/webhook", description="Webhook path")
    webapp_host: str = Field(default="0.0.0.0", description="Web app host")
    webapp_port: int = Field(default=8080, description="Web app port")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )


# Create settings instance
settings = Settings()
