from pydantic import BaseModel
from typing import List


class Weather(BaseModel):
    Type: str
    Date: str
    Rainfall: float


class WeatherList(BaseModel):
    Weather: List[Weather]


class Property(BaseModel):
    WeatherAreaCode: int
    WeatherList: WeatherList


class Geometry(BaseModel):
    Type: str
    Coordinates: str


class Feature(BaseModel):
    Id: str
    Name: str
    Geometry: Geometry
    Property: Property


class ResultInfo(BaseModel):
    Count: int
    Total: int
    Start: int
    Status: int
    Latency: float
    Description: str


class YDF(BaseModel):
    """
    YOLP 気象情報APIのレスポンス
    """

    ResultInfo: ResultInfo
    Feature: List[Feature]
