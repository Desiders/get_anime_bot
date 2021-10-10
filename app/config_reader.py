import dataclasses
import os


@dataclasses.dataclass(frozen=True)
class Bot:
    token: str


@dataclasses.dataclass(frozen=True)
class Database:
    host: str
    port: int
    db: int
    password: str


@dataclasses.dataclass(frozen=True)
class Config:
    bot: Bot
    database: Database


def load_config() -> Config:
    return Config(
        bot=Bot(
            token=os.getenv("BOT_TOKEN"),
        ),
        database=Database(
            host=os.getenv("HOST"),
            port=int(os.getenv("PORT")),
            db=int(os.getenv("DB")),
            password=os.getenv("PASSWORD"),
        ),
    )
