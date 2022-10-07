import operator

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column, Radio
from aiogram_dialog.widgets.text import Format, Multi
from app.domain.media.models import StatsType
from app.infrastructure.database.repositories.uow import UnitOfWork
from app.states import Stats
from app.typehints import I18nGettext
from structlog import get_logger
from structlog.stdlib import BoundLogger

logger: BoundLogger = get_logger()


async def get_text(_: I18nGettext, **kwarg) -> dict[str, str]:
    return {
        "select_stats_type_text": _("Select a stats type:"),
        "finish_dialog_text": _("Finish the dialog"),
    }


async def get_stats_types(
    _: I18nGettext, **kwargs,
) -> dict[str,  list[tuple[str, str]]]:
    stats_types = [
        (_("Media in database"), StatsType.MEDIA.name),
        (_("Viewed media by me"), StatsType.VIEWED_BY_ME.name),
        (_("Viewed media by all"), StatsType.VIEWED_BY_ALL.name),
    ]

    return {
        "stats_types": stats_types,
    }


async def get_stats_text(
    _: I18nGettext, dialog_manager: DialogManager, **kwargs,
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

    text: str | None = None
    if stats_type_name == StatsType.MEDIA.name:
        stats = await uow.media.get_media_stats()
        text = _(
            "Total count: {stats.total}\n"
            "GIF count: {stats.gif}\n"
            "IMG count: {stats.img}\n"
            "ALL count: {stats.all}\n"
            "SFW count: {stats.sfw}\n"
            "NSFW count: {stats.nsfw}"
        ).format(
            stats=stats.total,
            gif=stats.gif,
            img=stats.img,
            all=stats.all,
            sfw=stats.sfw,
            nsfw=stats.nsfw,
        )
    elif stats_type_name == StatsType.VIEWED_BY_ME.name:
        stats = await uow.views.get_views_stats()
        text = _("Total count: {stats}").format(stats=stats)
    elif stats_type_name == StatsType.VIEWED_BY_ALL.name:
        stats = await uow.views.get_views_stats_by_tg_id(c.from_user.id)
        text = _("Total count: {stats}").format(stats=stats)
    else:
        raise NotImplementedError(
            f"Stats type `{stats_type_name}` is not implemented"
        )

    manager.data["stats_text"] = text

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
        Button(
            text=Format("{finish_dialog_text}"),
            id="finish",
            on_click=finish_dialog,
        ),
        getter=[get_text, get_stats_text, get_stats_types],
        state=Stats.select_stats_type,
    ),
)
