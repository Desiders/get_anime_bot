from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text

from .send import command_what
from .start import command_start
from .url import command_get_url


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(command_start, commands="start")
    dispatcher.register_message_handler(command_get_url, Text(startswith="/"))
    dispatcher.register_message_handler(command_what)
