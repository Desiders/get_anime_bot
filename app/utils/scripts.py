import typing

from aiogram import md, types

from ..services.urls import GetUrl


def sfw_genres_format_text() -> str:
    if GetUrl.sfw_genres_format_text is None:
        GetUrl.sfw_genres_format_text = ", ".join(
            "/{}".format(md.hbold(genre))
            for genre in GetUrl.sfw_genres
        )
    return GetUrl.sfw_genres_format_text


def get_genre_and_mode(command: str) -> typing.Tuple[str, str, bool]:
    genre, *args = command.rsplit("_full", maxsplit=1)
    genre = genre.lower()

    full = args != []

    genre_with_prefix = f"/{genre}"

    return genre_with_prefix, genre, full


def generate_key(
    key: str,
    param: typing.Union[str, int],
) -> str:
    return f"{key}:{param}"


def create_reply_keyboard_markup(
    keyboard: typing.List[typing.List[types.KeyboardButton]],
) -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        selective=True,
    )


def create_inline_keyboard_markup(
    inline_keyboard: typing.List[typing.List[types.InlineKeyboardButton]],
) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
