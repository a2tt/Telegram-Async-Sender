import time
import math
from collections.abc import Iterable
from typing import Union, List

import telegram
from telegram import ReplyKeyboardMarkup
from telegram.error import RetryAfter, TimedOut, NetworkError, Unauthorized

from configs import RETRY


def send_message(tokens: List, chat_id: Union[str, int], text: str,
                 parse_mode: str = None, reply_markup: list = None):
    """
    :param tokens: telegram token(s)
    :param chat_id: chat_id | channel_id | ...
    :param text: message to send
    :param parse_mode: 'HTML' | None
    :param reply_markup: list containing list. A list forms a row. (ex. [[opt1], [opt2, opt3]])
    """
    if not text:
        return None

    if isinstance(reply_markup, Iterable):
        reply_markup = ReplyKeyboardMarkup(reply_markup, one_time_keyboard=True)

    for split_text in split_message(text, parse_mode):
        for idx in range(0, RETRY):
            try:
                # rotate tokens to avoid rate limit exceeded
                bot = telegram.Bot(tokens[idx % len(tokens)])
                bot.send_message(chat_id=chat_id, text=split_text, timeout=5,
                                 parse_mode=parse_mode,
                                 reply_markup=reply_markup,
                                 disable_web_page_preview=True)
                break
            except Unauthorized:
                # bot was blocked by the user
                # or message with options isn't allowed at the chatting room
                #   (ex. using reply_markup message to channel)
                break
            except TimedOut:
                # there's a chance the message has already been sent
                break
            except (NetworkError, RetryAfter) as e:
                time.sleep(3)


def split_message(message, parse_mode) -> list:
    """ telegram.Bot.send_message can only send maximum 4096 characters """
    if parse_mode == 'HTML':
        yield message  # XXX HTML 종료 태그 위치로 나눠야 함
    else:  # plain text
        for i in range(math.ceil(len(message) / 4000)):
            yield message[4000 * i: 4000 * (i + 1)]
