from .api import callYahooWeather, callDiscord
import logging
from .schema import YDF
from .config import Config
import sqlite3
import pathlib
from datetime import datetime
from typing import List
from .schema import Weather


async def run():
    """
    entrypoint
    """
    logger = logging.getLogger(name="weather-discord")
    logging.basicConfig(level=logging.INFO)

    response_yahoo = await callYahooWeather()
    logger.info(f"yahoo respond with code: {response_yahoo.status_code}")
    logger.debug(f"yahoo respond with body:\n{response_yahoo.text}")
    ry_parsed = YDF(**response_yahoo.json())

    config = Config()
    weatherList = sorted(
        ry_parsed.Feature[0].Property.WeatherList.Weather, key=lambda x: x.Date
    )

    con = sqlite3.connect(pathlib.Path(config.DB_PATH))
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    try:
        # 1. weather(type, date, rainfall)テーブルがなければ作成する
        cur.execute(
            "CREATE TABLE IF NOT EXISTS weather(type TEXT, date TEXT PRIMARY KEY, rainfall REAL)"
        )

        # 2. Upsertする
        for weather in weatherList:
            cur.execute(
                "INSERT OR REPLACE INTO weather VALUES (?, ?, ?)",
                (weather.Type, weather.Date, weather.Rainfall),
            )
        con.commit()

        # 3. 現在の降雨量を取得
        currentWeather = [w for w in weatherList if w.Type == "observation"][0]
        logger.info(f"currentWeather: {currentWeather.__repr__()}")

        # 4. 直近の降雨量を取得
        prevWeather = cur.execute(
            "SELECT * FROM weather WHERE type = 'observation' AND date < ? ORDER BY date DESC LIMIT 1",
            (currentWeather.Date,),
        ).fetchone()

        # 5. 雨上がり
        if (
            prevWeather
            and currentWeather.Rainfall == 0.0
            and prevWeather["rainfall"] > 0.0
        ):
            response_discord = await callDiscord("雨が上がりました")
            logger.info(f"discord respond with code: {response_discord.status_code}")
            logger.debug(f"discord respond with body:\n{response_discord.text}")

        # 6. 5分後の降雨量を取得
        nextWeathers: List[Weather] = [w for w in weatherList if w.Type == "forecast"]

        # 7. 雨が近い
        for nextWeather in nextWeathers:
            if (
                nextWeather
                and currentWeather.Rainfall == 0.0
                and nextWeather.Rainfall > 0.0
            ):
                # yyyyMMddhhmi 8: -> hhmi
                delta = datetime.strptime(
                    nextWeather.Date[8:], "%H%M"
                ) - datetime.strptime(currentWeather.Date[8:], "%H%M")

                response_discord = await callDiscord(
                    f"{delta.seconds // 60}分後に雨が降り始めます(降水量: {nextWeather.Rainfall}mm/h)"
                )
                logger.info(
                    f"discord respond with code: {response_discord.status_code}"
                )
                logger.debug(f"discord respond with body:\n{response_discord.text}")
                break

        # 8. observationのデータが10件以上あるなら、新しい順に10件残して残りを削除する
        cur.execute(
            """
            DELETE FROM weather
            WHERE type = 'observation'
            AND date < (
                SELECT date FROM weather
                WHERE type = 'observation'
                ORDER BY date DESC
                LIMIT 1 OFFSET 9
            )
            """
        )
        con.commit()

    finally:
        cur.close()
        con.close()
