from aiogram import md, types

from ..utils import scripts, text


async def command_start(message: types.Message):
    await message.answer(
        text=text.get_text(
            language_code=message.from_user.language_code,
            text_name="start",
        ).format(
            full_name=md.quote_html(message.from_user.full_name),
            sfw_genres=scripts.sfw_genres_format_text(),
        ),
        parse_mode="HTML",
        reply_markup=types.ReplyKeyboardRemove(selective=True),
    )


async def command_about(message: types.Message):
    await message.answer(
        text=text.get_text(
            language_code=message.from_user.language_code,
            text_name="about",
        ),
        reply_markup=scripts.create_reply_keyboard_markup(
            keyboard=[
                [types.KeyboardButton("/start")],
            ]
        )
    )
