"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
import os

from dotenv import load_dotenv

BOT_TOKEN = os.getenv('BOT_TOKEN')

load_dotenv()

@dataclass(frozen=True)
class Settings:
    bot_token: str
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Settings":
        bot_token = BOT_TOKEN


        log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper() or "INFO"
        return cls(bot_token=bot_token, log_level=log_level)
