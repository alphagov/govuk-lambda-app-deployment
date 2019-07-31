## Lambda: DownloadLogsAnalytics

Uploads fastly asset logs to Google analytics.

The Lambda takes logs from the govuk-analytics-logs-production<br/>bucket and uploads them to Google analytics everytime a new log<br/>file is created in the bucket, which is currently every minute.

### Making changes

This lambda is currently not managed in terraform, so any changes<br/>to the python code are pushed to AWS using ```deploy.sh```.

### Dependencies

Python 3.7  
VirtualEnv  
Pip
