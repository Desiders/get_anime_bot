from aiogram.types import User
from aiogram_dialog import Dialog, Window
from aiogram_dialog.dialog import DialogManager
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Format
from app.states import Language, MainMenu, Settings, Stats
from app.typehints import I18nGettext


async def get_text(
    _: I18nGettext,
    dialog_manager: DialogManager,
    **kwargs,
) -> dict[str, str]:
    data = dialog_manager.current_context().start_data  # type: ignore
    user: User = data["user"]  # type: ignore

    return {
        "start_text": _(
            "Hi, {first_name}!\n\n"
            "Get an anime GIF or image by genre!\n"
            "/genres_gif\n"
            "/genres_img\n"
            "/genres_all"
        ).format(
            first_name=user.first_name,
        ),
        "language_text": _("Change language"),
        "settings_text": _("Change settings"),
        "stats_text": _("View statistics"),
    }


main_menu = Dialog(
    Window(
        Format("{start_text}"),
        Start(
            Format("{language_text}"),
            id="change_language",
            state=Language.select_language,
        ),
        Start(
            Format("{settings_text}"),
            id="change_settings",
            state=Settings.select_settings,
        ),
        Start(
            Format("{stats_text}"),
            id="view_stats",
            state=Stats.select_stats_type,
        ),
        getter=get_text,
        state=MainMenu.main_menu,
    ),
)
