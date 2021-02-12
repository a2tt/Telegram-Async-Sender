from helpers.aws_lambda import unpack
from tasks.telegram_bot import send_message


def send(event=None, context=None):
    print(event)
    for record in event['Records']:
        print('---')
        record_data = unpack(record)
        data = record_data['data']

        print(data)
        send_message(**data)
