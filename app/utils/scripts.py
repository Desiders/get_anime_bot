from typing import Tuple, Union

from aiogram import md

from ..services.urls import GetUrl


def genres_format_text() -> str:
    if GetUrl.genres_format_text is None:
        sep, prefix = ", ", "/"
        genres = sep.join(
            f"{prefix}{md.hbold(url)}"
                for url in GetUrl.genres
        )
        GetUrl.genres_format_text = genres
    return GetUrl.genres_format_text


def get_genre_and_mode(text: str) -> Tuple[str, str, bool]:
    if text.endswith("_full"):
        full = True
        genre, _ = text.split("_")
    else:
        full = False
        genre = text
    genre_with_prefix = genre
    genre_without_prefix = genre[1:]
    return genre_with_prefix, genre_without_prefix, full


def generate_key(key: str, param: Union[str, int]) -> str:
    return f"{key}:{param}"
