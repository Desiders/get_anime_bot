from aiogram import Dispatcher
from aiogram.types import Update
from aiogram_dialog.exceptions import UnknownIntent
from app.typehints import I18nGettext
from structlog import get_logger
from structlog.stdlib import BoundLogger

logger: BoundLogger = get_logger()


async def dialog_exception(u: Update, exc: UnknownIntent) -> bool:
    _: I18nGettext = u.bot["gettext"]

    await u.callback_query.answer(
        text=_(
            "It looks like this message belongs to another person "
            "or something went wrong"
        ),
        show_alert=True,
        cache_time=60,
    )

    return True


def register_error_handlers(dp: Dispatcher):
    dp.register_errors_handler(dialog_exception, exception=UnknownIntent)
