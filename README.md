# Telegram-Async-Sender

Telegram-Async-Sender for building asynchronous telegram sender using AWS SQS + Lambda.  
When you enqueue messages to AWS SQS, the SQS triggers Lambda and the Lambda sends telegram messages to the specified chat room.


# Requirements
1. Install [serverless](https://www.serverless.com/framework/docs/getting-started) framework.   
    ```
   $ npm install -g serverless
    ```
2. configure [AWS configuration and credential files](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)


# Deployment
1. Copy `configs.yml.example` to `configs.yml`
2. Modify `configs.yml` for external reference in `serverless.yml`
3. Let's deploy
    - if you use AWS Lambda layers and configured in `configs.yml`, deploy with the following command  
        ```
       $ serverless deploy -v
        ```
       > [lambda layers](https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/configuration-layers.html), [serverless](https://www.serverless.com/framework/docs/providers/aws/guide/layers)
    - or you can use `serverless-python-requirements`
       > [documents](https://www.serverless.com/plugins/serverless-python-requirements) 
    - or you can deploy(upload) `.zip` package manually
       > [documents](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)

# Usage
1. Copy and paste `./helpers/aws_sqs.py` to your client project.
2. Send message to SQS like following code. 
    ```python
    # ./helpers/aws_sqs.py
    data = {
        'token': '<token>',  # list | str
        'chat_id': '<chat_id>',  # list | str | int
        'text': 'message to send',  # str
        'parse_mode': 'HTML',  # 'HTML' | 'MarkDown' | None (default: None)
        'reply_markup': None,  # list | None (default: None)
    }
    sqs_send_message(data, '<your_queue_name>')
    ```
3. Then the SQS will receive the message and trigger Lambda.
4. The Lambda sends telegram messages to the specified chat room.
