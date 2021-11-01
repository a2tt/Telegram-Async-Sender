import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

import configs


def init_sentry():
    sentry_sdk.init(
        dsn=configs.SENTRY_DSN,
        integrations=[AwsLambdaIntegration()]
    )
