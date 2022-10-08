import operator

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Radio
from aiogram_dialog.widgets.text import Format
from app.infrastructure.database.repositories.uow import UnitOfWork
from app.language_utils.language import AVAILABLE_LANGUAGES
from app.middlewares import I18nMiddleware
from app.states import Language
from app.typehints import I18nGettext


async def get_text(_: I18nGettext, **kwargs) -> dict[str, str]:
    return {
        "select_language_text": _("Select a language:"),
        "cancel_text": _("Go back"),
    }


async def get_languages(
    _: I18nGettext, **kwargs,
) -> dict[str,  list[tuple[str | None, str]]]:
    languages = [
        (lang.label, lang.code)
        for lang in AVAILABLE_LANGUAGES.values()
    ]

    return {
        "languages": languages,
    }


async def select_language(
    c: CallbackQuery,
    button: Radio,
    manager: DialogManager,
    language_code: str,
):
    if button.get_checked(manager) == language_code:
        await c.answer()
        return

    i18n: I18nMiddleware = c.bot["i18n"]
    i18n.change_user_locale(language_code)

    uow: UnitOfWork = c.bot["uow"]

    await uow.users.update_language_code(
        c.from_user.id, language_code,
    )
    await uow.commit()

    await c.answer()


async def finish_dialog(
    c: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    await c.message.delete()
    await manager.done()


language = Dialog(
    Window(
        Format("{select_language_text}"),
        Radio(
            checked_text=Format("✓ {item[0]}"),
            unchecked_text=Format("{item[0]}"),
            id="select_language",
            item_id_getter=operator.itemgetter(1),
            items="languages",
            on_click=select_language,  # type: ignore
        ),
        Cancel(Format("{cancel_text}")),
        getter=[get_text, get_languages],
        state=Language.select_language,
    ),
)
