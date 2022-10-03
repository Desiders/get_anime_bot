import operator

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.kbd import Button, Column, Radio
from aiogram_dialog.widgets.text import Format
from app.infrastructure.database.repositories.uow import UnitOfWork
from app.language_utils.language import AVAILABLE_LANGUAGES
from app.middlewares import I18nMiddleware
from app.typehints import I18nGettext


class Language(StatesGroup):
    main = State()


async def get_data(_: I18nGettext, **kwargs):
    languages = [
        (lang.label, lang.code)
        for lang in AVAILABLE_LANGUAGES.values()
    ]

    select_language_text = _("Select a language:")
    finish_dialog_text = _("Finish dialog")

    return {
        "languages": languages,
        "select_language_text": select_language_text,
        "finish_dialog_text": finish_dialog_text,
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


dialog = Dialog(
    Window(
        # "Select a language:"
        Format("{select_language_text}"),
        Radio(
            checked_text=Format("✓ {item[0]}"),
            unchecked_text=Format("{item[0]}"),
            id="language",
            item_id_getter=operator.itemgetter(1),
            items="languages",
            on_click=select_language,
        ),
        Column(
            Button(
                # "Finish dialog"
                text=Format("{finish_dialog_text}"),
                id="finish",
                on_click=finish_dialog,
            ),
        ),
        state=Language.main,
        getter=get_data,
        parse_mode="HTML",
        disable_web_page_preview=True,
    ),
    launch_mode=LaunchMode.STANDARD,
)
