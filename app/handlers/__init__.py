from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text

from . import send, start, url


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(start.command_start, commands="start")
    dispatcher.register_message_handler(send.command_reset, commands="reset")
    dispatcher.register_message_handler(url.command_get_url, Text(startswith="/"))
    dispatcher.register_message_handler(send.command_what, chat_type="private")
