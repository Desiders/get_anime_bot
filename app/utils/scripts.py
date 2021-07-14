import collections
from typing import List, Optional, Tuple, Union

from aiogram import md
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from .. import texts
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


def get_language(lang_code: Optional[str]) -> str:
    languages = collections.defaultdict(
        lambda: "en", dict(ru="ru")
    )
    return languages[lang_code.split("-")[0]] if lang_code else "en"


def get_text(lang_code: Optional[str], text_name: str) -> str:
    language = get_language(lang_code)
    text = texts.all_texts[language][text_name]
    return text


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
