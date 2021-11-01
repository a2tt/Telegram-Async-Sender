from typing import Union, List

from sentry_sdk import capture_exception

from helpers.aws_lambda import unpack
from helpers.sentry import init_sentry
from tasks.telegram_bot import send_message

init_sentry()


def send(event=None, context=None):
    for record in event['Records']:
        print(record)
        try:
            # unpack SQS message
            record_data = unpack(record)
            data = record_data['data']

            # prepare configs and data
            telegram_tokens: Union[List, str] = data.get('token')
            if type(telegram_tokens) != list:
                telegram_tokens = [telegram_tokens]

            chat_ids: Union[List, str] = data.get('chat_id')
            if type(chat_ids) != list:
                chat_ids = [chat_ids]

            text = data.get('text')

            # validation
            if not text or not chat_ids or not telegram_tokens:
                raise ValueError('Can\'t send message. (Value is missing)')

            # send message
            for chat_id in chat_ids:  # available to send message to multiple users or channels
                send_message(tokens=telegram_tokens, chat_id=chat_id, text=text,
                             parse_mode=data.get('parse_mode'), reply_markup=data.get('reply_markup'))
        except Exception as e:
            capture_exception(e)


if __name__ == '__main__':
    _token = ''
    _chat_id = ''

    send(event={
        'Records': [
            {
                'body': {
                    'token': _token,
                    'chat_id': _chat_id,
                    'text': '<a href="https://google.com">test message</a>',
                    'parse_mode': None,
                    'reply_markup': [['opt1'], ['opt2', 'opt3']]
                }
            },
            {
                'body': {
                    'token': [_token],
                    'chat_id': [_chat_id, _chat_id],
                    'text': '<a href="https://google.com">test message 2</a>',
                    'parse_mode': 'HTML',
                }
            },
        ]
    })
