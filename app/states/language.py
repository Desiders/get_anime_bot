from aiogram.dispatcher.filters.state import State, StatesGroup


class Language(StatesGroup):
    select_language = State()
