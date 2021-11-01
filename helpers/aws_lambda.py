import json


def unpack(record) -> dict:
    try:
        data = json.loads(record['body'])
    except (json.decoder.JSONDecodeError, TypeError):
        data = record['body']

    return {
        'data': data,
    }
