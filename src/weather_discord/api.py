"""
api call funcitons.
"""

import httpx
from .config import Config
import json


async def callYahooWeather() -> httpx.Response:
    """
    call yahoo weather api.
    """
    config = Config()
    params = {
        "appid": config.YAHOO_CLIENT_ID,
        "coordinates": f"{config.LONGITUDE},{config.LATITUDE}",
        "output": "json",
        "interval": config.INTERVAL,
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(config.YAHOO_ENDPOINT_URL, params=params)
            return response
        except Exception as _:
            raise


async def callDiscord(message: str) -> httpx.Response:
    """
    call discord webhook api.
    """
    config = Config()
    body = {"content": message}
    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                config.DISCORD_WEBHOOK_URL, content=json.dumps(body), headers=headers
            )
            return response
        except Exception as _:
            raise
