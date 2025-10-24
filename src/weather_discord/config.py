from dotenv import load_dotenv
import os
from .exception import ConfigException


load_dotenv()


def _get_config(name: str) -> str:
    config = os.getenv(name)
    if config is None:
        raise ConfigException(f"{name} is not set.")
    return config


class Config:
    # environment variables
    DISCORD_WEBHOOK_URL: str
    YAHOO_CLIENT_ID: str
    LONGITUDE: str
    LATITUDE: str
    DB_PATH: str

    # constants
    YAHOO_ENDPOINT_URL: str = "https://map.yahooapis.jp/weather/V1/place"
    INTERVAL: int = 5

    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.DISCORD_WEBHOOK_URL = _get_config("DISCORD_WEBHOOK_URL")
            cls._instance.YAHOO_CLIENT_ID = _get_config("YAHOO_CLIENT_ID")
            cls._instance.LONGITUDE = _get_config("LONGITUDE")
            cls._instance.LATITUDE = _get_config("LATITUDE")
            cls._instance.DB_PATH = _get_config("DB_PATH")
        return cls._instance
