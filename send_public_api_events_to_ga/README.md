## Send public API events to analytics

This lambda function processes logs in the S3 bucket `govuk-analytics-logs-production`.

It is triggered by `ObjectCreated` events on the bucket, it will only process S3 objects with the prefix `public_api_logs/`.

### Deployment

Python 3.6 is required to deploy this lambda.
If you don't have 3.6, [pyenv](https://github.com/pyenv/pyenv) is a useful library for Python version management.

You'll also need to install and configure the AWS CLI with the appropriate credentials.

The deploy script will create a virtualenv, install dependencies and publish the lambda to AWS.

```
./deploy.sh
```

### Tests

```
pip install nosetest # You only need to do this once.

nosetest test_send_public_api_events_to_ga.py
```
