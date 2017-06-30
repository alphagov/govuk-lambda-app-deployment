from .base import Base
import gzip
import os
import csv
import requests
import urllib.parse
from io import TextIOWrapper
import grequests

import boto3
s3 = boto3.client('s3')


class AWSLambda(Base):
    def __init__(self, bucket, filename):
        self.bucket = bucket
        super().__init__(filename)

    def open_for_read(self):
        obj = s3.get_object(Bucket=self.bucket, Key=self.filename)
        return TextIOWrapper(gzip.GzipFile(fileobj=obj['Body'], mode='r'))

    def process(self):
        csvreader = csv.reader(self.open_for_read(), delimiter="\t")
        data = []

        for row in csvreader:
            result = self.transform_row(row)
            if result is not '' and result is not None:
                data.append(result)

        return data

    def parse_row(self, row):
        if row['ga_client_id'] != '':
            row['ga_client_id'] = self.parse_client_id(row['ga_client_id'])
        return row

    def parse_client_id(self, client_id):
        client_id = client_id.replace('GA', '')
        client_id = client_id.split(".")[-2:]
        return ".".join(client_id)

    def construct_url(self, download_data):
        property_id = 'UA-26179049-7'
        ga_client_id = download_data['ga_client_id'] or 'No client id'
        category = 'Download from External Source'
        filename = download_data['file_downloaded'] or 'No filename present'
        referrer = download_data['referrer'] or 'No referrer'
        user_agent = download_data['user_agent'] or 'No user agent'

        params = urllib.parse.urlencode({
                                        'v': 1,
                                        'tid': property_id,
                                        'cid': ga_client_id,
                                        't': 'event',
                                        'ec': category,
                                        'ea': filename,
                                        'el': referrer,
                                        'cd13': user_agent,
                                        'ua': user_agent
                                        })
        return "http://www.google-analytics.com/collect?{0}".format(params)

    def send_events_to_GA(self):
        rows = self.process()
        urls = []
        for row in rows:
            download_data = self.parse_row(row)
            url = self.construct_url(self, download_data)
            urls.append(url)

        rs = [grequests.post(u) for u in urls]

        return grequests.map(rs)



