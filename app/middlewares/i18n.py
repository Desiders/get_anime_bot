from aiogram.contrib.middlewares.i18n import I18nMiddleware as BaseI18nMiddleware
from aiogram.types import CallbackQuery, Message
from app.infrastructure.database.models import UserModel
from app.infrastructure.database.repositories.uow import UnitOfWork
from app.language_utils.language import get_locale_or_default


class I18nMiddleware(BaseI18nMiddleware):
    async def get_user_locale(self, action, args: tuple) -> str | None:
        obj: CallbackQuery | Message
        data: dict
        obj, *_, data = args

        user: UserModel | None = data.get("user")
        if user is None:
            return None

        if not (language_code := user.language_code):
            language_code = get_locale_or_default(obj.from_user.locale)

            uow: UnitOfWork = data["uow"]

            await uow.users.update_language_code(
                user.tg_id,
                language_code,  # type: ignore
            )
            await uow.commit()

            user.language_code = language_code  # type: ignore
            data["user"] = user

        data["_"] = self.gettext
        obj.bot["gettext"] = self.gettext
        obj.bot["i18n"] = self

        return language_code  # type: ignore

    def change_user_locale(self, locale: str):
        self.ctx_locale.set(locale)  # type: ignore
