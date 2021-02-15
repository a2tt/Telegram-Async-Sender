import typing
import time
import math
from collections.abc import Iterable

import telegram
from telegram import ReplyKeyboardMarkup
from telegram.error import RetryAfter, TimedOut, NetworkError, Unauthorized

from configs import RETRY


def send_message(token: str, chat_id: typing.Union[int, str], text: str,
                 parse_mode: str = None, reply_markup: list = None):
    """
    :param token: telegram token
    :param chat_id: chat_id | channel_id | ...
    :param text:
    :param parse_mode: None | 'HTML'
    :param reply_markup: list containing list. A list forms a row.
    """
    bot = telegram.Bot(token)

    if not text:
        return None

    if isinstance(reply_markup, Iterable):
        reply_markup = ReplyKeyboardMarkup(reply_markup, one_time_keyboard=True)

    splitted = split_message(text, parse_mode)
    for msg in splitted:
        for idx in range(0, RETRY):
            try:
                bot.send_message(chat_id=chat_id, text=msg, timeout=5,
                                 parse_mode=parse_mode,
                                 reply_markup=reply_markup,
                                 disable_web_page_preview=True)
                break
            except Unauthorized:  # bot was blocked by the user
                break   
            except TimedOut:  # 요청이 갔을 가능성이 있으므로
                break
            except (NetworkError, RetryAfter) as e:
                time.sleep(5)


def split_message(message, parse_mode):
    """ telegram.Bot.send_message can send max 4096 characters """
    messages = []

    if parse_mode == 'HTML':
        messages.append(message)  # XXX HTML 종료 태그 위치로 나눠야 함
    else:  # plain text
        for i in range(math.ceil(len(message) / 4000)):
            messages.append(message[4000 * i: 4000 * (i + 1)])
    return messages
