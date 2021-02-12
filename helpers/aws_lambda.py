import json


def unpack(record):
    try:
        data = json.loads(record['body'])
    except json.decoder.JSONDecodeError:
        data = record['body']

    return {
        'data': data,
    }
