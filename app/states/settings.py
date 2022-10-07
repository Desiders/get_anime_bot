from aiogram.dispatcher.filters.state import State, StatesGroup


class Settings(StatesGroup):
    select_settings = State()
