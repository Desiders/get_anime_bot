from dataclasses import dataclass
from os import getenv


@dataclass
class Bot:
    token: str


@dataclass
class Database:
    host: str
    port: int
    db: int
    password: str


@dataclass
class Config:
    bot: Bot
    database: Database


def load_config() -> Config:
    config = Config(
        bot=Bot(
            token=getenv("BOT_TOKEN")
        ),
        database=Database(
            host=getenv("HOST"),
            port=int(getenv("PORT")),
            db=int(getenv("DB")),
            password=getenv("PASSWORD")
        )
    )
    return config
