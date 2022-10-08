import operator

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Radio
from aiogram_dialog.widgets.text import Format
from app.infrastructure.database.repositories.uow import UnitOfWork
from app.states import Settings
from app.typehints import I18nGettext


async def get_text(_: I18nGettext, **kwargs) -> dict[str, str]:
    return {
        "choice_settings_text": _("Choose your settings:"),
        "cancel_text": _("Go back"),
    }


async def get_settings(
    _: I18nGettext, **kwargs,
) -> dict[str, list[tuple[str,  str]]]:
    nsfw_settings = [
        (_("Show NSFW"), "show"),
        (_("Hide NSFW"), "hide"),
    ]

    return {
        "nsfw_settings": nsfw_settings,
    }


async def select_nsfw_setting(
    c: CallbackQuery,
    button: Radio,
    manager: DialogManager,
    nsfw_setting: str,
):
    if button.get_checked(manager) == nsfw_setting:
        await c.answer()
        return

    uow: UnitOfWork = c.bot["uow"]

    await uow.users.update_show_nsfw(
        tg_id=c.from_user.id,
        show_nsfw=nsfw_setting == "show",
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


settings = Dialog(
    Window(
        Format("{choice_settings_text}"),
        Radio(
            checked_text=Format("✓ {item[0]}"),
            unchecked_text=Format("{item[0]}"),
            id="select_nsfw_setting",
            item_id_getter=operator.itemgetter(1),
            items="nsfw_settings",
            on_click=select_nsfw_setting,  # type: ignore
        ),
        Cancel(Format("{cancel_text}")),
        getter=[get_text, get_settings],
        state=Settings.select_settings,
    ),
)
