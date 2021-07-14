from aiogram import Dispatcher

from ..filters import CheckCommandFilter
from . import send, start, url


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start.command_start, commands="start")
    dispatcher.register_message_handler(start.command_about, commands=['about', 'source'])
    dispatcher.register_message_handler(send.command_reset, commands="reset")
    dispatcher.register_message_handler(url.command_sfw_get_url, CheckCommandFilter("sfw"))
    dispatcher.register_message_handler(url.command_nsfw_get_url, CheckCommandFilter("nsfw"),
                                        chat_type="private")
    dispatcher.register_callback_query_handler(url.command_send_nsfw_url)
