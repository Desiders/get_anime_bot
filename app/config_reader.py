from pydantic import BaseSettings


class Bot(BaseSettings):
    token: str


class Database(BaseSettings):
    user: str
    password: str
    host: str
    port: int
    name: str


class SettingsExtractor(BaseSettings):
    # telegram bot
    BOT_TOKEN: str

    # database
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str


class Settings(BaseSettings):
    bot: Bot
    database: Database

    class Config:
        env_file_encoding = "utf-8"


def load_config() -> Settings:
    settings = SettingsExtractor()

    return Settings(
        bot=Bot(token=settings.BOT_TOKEN),
        database=Database(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            name=settings.DB_NAME,
        ),
    )
