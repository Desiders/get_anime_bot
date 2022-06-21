from configparser import ConfigParser
from typing import Union

from pydantic import BaseModel


class Bot(BaseModel):
    token: str


class Database(BaseModel):
    driver: str
    user: str
    password: str
    host: str
    port: Union[str, int]
    name: str


class Config(BaseModel):
    bot: Bot
    database: Database


def load_config(path: str) -> Config:
    config = ConfigParser()
    config.read(path)

    bot = config["bot"]
    database = config["database"]

    return Config(
        bot=Bot(
            token=bot["token"],
        ),
        database=Database(
            driver=database["driver"],
            user=database["user"],
            password=database["password"],
            host=database["host"],
            port=database["port"],
            name=database["name"],
        ),
    )
