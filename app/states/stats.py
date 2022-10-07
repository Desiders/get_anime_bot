from aiogram.dispatcher.filters.state import State, StatesGroup


class Stats(StatesGroup):
    select_stats_type = State()
