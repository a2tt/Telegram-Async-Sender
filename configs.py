import yaml

with open('configs.yml', 'rt') as fp:
    configs_yml = yaml.safe_load(fp)

RETRY = 5
SQS_REGION = configs_yml['provider']['region']
