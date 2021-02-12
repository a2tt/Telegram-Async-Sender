import json

import boto3

sqs = boto3.resource('sqs', region_name='ap-northeast-2')

required_key = ['token', 'recv_id', 'message']


def send_sqs(data: dict, queue_name: str):
    if not data:
        return

    for key in required_key:
        if key not in data:
            return

    queue = sqs.get_queue_by_name(QueueName=queue_name)
    try:
        queue.send_message(
            MessageBody=json.dumps(data),
            DelaySeconds=0,
        )
    except Exception as e:
        print(e)
