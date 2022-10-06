import operator

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.kbd import Button, Column, Radio
from aiogram_dialog.widgets.text import Format
from app.infrastructure.database.repositories.uow import UnitOfWork
from app.typehints import I18nGettext


class Settings(StatesGroup):
    main = State()


async def get_data(_: I18nGettext, **kwargs):
    show_nsfw_settings = [
        (_("Show nsfw"), "show"),
        (_("Hide nsfw"), "hide"),
    ]

    choice_settings_text = _("Choose your settings:")
    finish_dialog_text = _("Finish dialog")

    return {
        "show_nsfw_settings": show_nsfw_settings,
        "choice_settings_text": choice_settings_text,
        "finish_dialog_text": finish_dialog_text,
    }


async def select_show_nsfw_setting(
    c: CallbackQuery,
    button: Radio,
    manager: DialogManager,
    show_nsfw_string: str,
):
    if button.get_checked(manager) == show_nsfw_string:
        await c.answer()
        return

    show_nsfw = show_nsfw_string == "show"

    uow: UnitOfWork = c.bot["uow"]

    await uow.users.update_show_nsfw(
        c.from_user.id, show_nsfw,
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
        # "Choose your settings:"
        Format("{choice_settings_text}"),
        Radio(
            checked_text=Format("✓ {item[0]}"),
            unchecked_text=Format("{item[0]}"),
            id="show_nsfw",
            item_id_getter=operator.itemgetter(1),
            items="show_nsfw_settings",
            on_click=select_show_nsfw_setting,  # type: ignore
        ),
        Column(
            Button(
                # "Finish dialog"
                text=Format("{finish_dialog_text}"),
                id="finish",
                on_click=finish_dialog,
            ),
        ),
        state=Settings.main,
        getter=get_data,
        parse_mode="HTML",  # type: ignore
        disable_web_page_preview=True,
    ),
    launch_mode=LaunchMode.STANDARD,
)
