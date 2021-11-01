import json

import boto3
import configs

sqs = boto3.resource('sqs', region_name=configs.SQS_REGION)

required_key = ['token', 'chat_id', 'message']


def sqs_send_message(data: dict, queue_name: str):
    """
    Delivers a message to the specified queue.
    See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#service-resource
        and https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#service-resource
    """
    if not data:
        return

    for key in required_key:
        if key not in data:
            raise ValueError(f'`{key}` required to send telegram.')

    queue = sqs.get_queue_by_name(QueueName=queue_name)
    try:
        queue.send_message(
            MessageBody=json.dumps(data),
            DelaySeconds=0,
        )
    except Exception as e:
        print(e)
