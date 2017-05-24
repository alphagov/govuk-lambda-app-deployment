import re
import sys
from urllib.parse import unquote

from govuk_logs.cli import Cli
from govuk_logs.aws_lambda import AWSLambda

EVENT_REGEX = re.compile(r'^ObjectCreated:')

def handle_lambda(event, context):
    if event['Records']:
        for record in event['Records']:
            if EVENT_REGEX.match(record['eventName']):
                runner = AWSLambda(record['s3']['bucket']['name'], unquote(record['s3']['object']['key']))
                runner.process()

def handle_cli(bucket, filename):
    runner = AWSLambda(bucket, filename)
    runner.process()


if __name__ == "__main__":
    handle_cli(sys.argv[1], sys.argv[2])
