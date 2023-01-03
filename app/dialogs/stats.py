import operator

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Column, Radio
from aiogram_dialog.widgets.text import Format, Multi
from app.domain.media.models import StatsType
from app.infrastructure.database.repositories.uow import UnitOfWork
from app.media_utils import get_stats_text as get_media_stats_text
from app.states import Stats
from app.typehints import I18nGettext
from structlog import get_logger
from structlog.stdlib import BoundLogger

logger: BoundLogger = get_logger()


async def get_text(_: I18nGettext, **kwargs) -> dict[str, str]:
    return {
        "select_stats_type_text": _("Select a stats type:"),
        "cancel_text": _("Go back"),
    }


async def get_stats_types(
    _: I18nGettext,
    **kwargs,
) -> dict[str, list[tuple[str, str]]]:
    stats_types = [
        (_("Media in database"), StatsType.MEDIA.name),
        (_("Viewed media by me"), StatsType.VIEWED_BY_ME.name),
        (_("Viewed media by all"), StatsType.VIEWED_BY_ALL.name),
    ]

    return {
        "stats_types": stats_types,
    }


async def get_stats_text(
    _: I18nGettext,
    dialog_manager: DialogManager,
    **kwargs,
) -> dict[str, str | bool]:
    if stats_text := dialog_manager.data.get("stats_text"):
        return {
            "stats_text": stats_text,
            "has_stats_text": True,
        }
    return {
        "has_stats_text": False,
    }


async def select_stats_type(
    c: CallbackQuery,
    button: Radio,
    manager: DialogManager,
    stats_type_name: str,
):
    uow: UnitOfWork = c.bot["uow"]
    _: I18nGettext = c.bot["gettext"]

    if stats_type_name == StatsType.MEDIA.name:
        stats = await uow.media.get_media_stats()
    elif stats_type_name == StatsType.VIEWED_BY_ME.name:
        stats = await uow.media.get_viewed_media_stats_by_tg_id(c.from_user.id)
    elif stats_type_name == StatsType.VIEWED_BY_ALL.name:
        stats = await uow.media.get_viewed_media_stats()
    else:
        raise NotImplementedError(f"Stats type `{stats_type_name}` is not implemented")

    manager.data["stats_text"] = get_media_stats_text(stats, _)

    await c.answer(cache_time=1)


async def finish_dialog(
    c: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    await c.message.delete()
    await manager.done()


stats = Dialog(
    Window(
        Multi(
            Format(
                "{stats_text}",
                when="has_stats_text",
            ),
            Format("{select_stats_type_text}"),
            sep="\n\n",
        ),
        Column(
            Radio(
                checked_text=Format("✓ {item[0]}"),
                unchecked_text=Format("{item[0]}"),
                id="select_stats_type",
                item_id_getter=operator.itemgetter(1),
                items="stats_types",
                on_click=select_stats_type,  # type: ignore
            ),
        ),
        Cancel(Format("{cancel_text}")),
        getter=[get_text, get_stats_text, get_stats_types],
        state=Stats.select_stats_type,
    ),
)
