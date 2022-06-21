import operator

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.kbd import Radio
from aiogram_dialog.widgets.text import Const, Format
from app.infrastructure.database.repositories.uow import UnitOfWork
from app.middlewares import I18nMiddleware
from app.utils.language import AVAILABLE_LANGUAGES


class Language(StatesGroup):
    main = State()
    select = State()


async def get_data(**kwargs):
    languages = [
        (lang.label, lang.code)
        for lang in AVAILABLE_LANGUAGES.values()
    ]

    return {
        "languages": languages,
        "count": len(languages),
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


dialog = Dialog(
    Window(
        Const("Select a language:"),
        Radio(
            checked_text=Format("✓ {item[0]}"),
            unchecked_text=Format("{item[0]}"),
            id="language",
            item_id_getter=operator.itemgetter(1),
            items="languages",
            on_click=select_language,
        ),
        state=Language.main,
        getter=get_data,
        parse_mode="HTML",
        disable_web_page_preview=True,
    ),
    launch_mode=LaunchMode.STANDARD,
)
