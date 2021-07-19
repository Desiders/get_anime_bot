from typing import List, Tuple, Union

from aiogram import md
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from ..services.urls import GetUrl


def sfw_genres_format_text() -> Tuple[str]:
    if GetUrl.sfw_genres_format_text is None:
        sep, prefix = ", ", "/"
        sfw_genres = sep.join(
            f"{prefix}{md.hbold(url)}"
                for url in GetUrl.sfw_genres
        )
        GetUrl.sfw_genres_format_text = sfw_genres
    return GetUrl.sfw_genres_format_text


def get_genre_and_mode(command: str) -> Tuple[str, str, bool]:
    command, *args = command.split("_full")
    full = args != []
    genre = command.lower()
    genre_with_prefix = f"/{genre}"
    genre_without_prefix = genre
    return genre_with_prefix, genre_without_prefix, full


def generate_key(key: str, param: Union[str, int]) -> str:
    return f"{key}:{param}"


def create_reply_keyboard_markup(keyboard: List[List[KeyboardButton]]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        selective=True
    )
    return markup


def create_inline_keyboard_markup(inline_keyboard: List[List[InlineKeyboardButton]]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return markup
