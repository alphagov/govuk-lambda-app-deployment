#! /bin/bash

rm -rf .venv function.zip

virtualenv .venv
. .venv/bin/activate
pip install -r requirements.txt

zip -r function.zip send_public_api_events_to_ga.py -x *.pyc -x *.log -x *.txt.gz -x test_requirements.txt
(
  cd .venv/lib/python3.7/site-packages
  zip -r ../../../../function.zip * -x *.pyc
)

pip download --platform manylinux1_x86_64 --only-binary :all: --abi cp37m $(cat binary_requirements.txt)
mkdir -p wheelhouse
ls *.whl | xargs -I '{}' -n1 unzip {} -d wheelhouse
rm *.whl
(
  cd wheelhouse
  zip -r ../function.zip *
)
rm -rf wheelhouse

# Manual way to deploy lambda function code
# aws lambda update-function-code --function-name SendPublicAPIEventsToGA --zip-file fileb://function.zip --publish

# Deploy this to a specific S3 bucket for execution.
# See alphagov/govuk-terraform-provisioning/projects/analytics_lambdas
aws s3 cp function.zip s3://govuk-analytics-logs-production/send_public_api_events_to_ga_lambda.zip

rm function.zip
