import csv
from io import BytesIO, TextIOWrapper
import json
import os
import os.path
import threading
from urllib.parse import parse_qsl

class Base(object):

    def __init__(self, filename):
        self.filename = filename

    def open_for_read(self):
        raise NotImplementedError

    def open_for_write(self, path):
        raise NotImplementedError

    def process(self):
        path = os.path.dirname(self.filename)
        name = os.path.basename(self.filename)
        date, rest = name.split('T', maxsplit=1)
        y, m, d = date.split('-')

        rest = rest.replace('.log.gz', '.json.gz')

        new_path = 'year={}/month={}/date={}/{}'.format(y, m, d, rest)

        csvreader = csv.reader(self.open_for_read(), delimiter="\t")

        data = "\n".join([json.dumps(self.transform_row(row)) for row in csvreader])

        self.put_to_s3(new_path, data)


    def transform_row(self, row):
        try:
            timestamp, querystring, ip, uri, user_agent = row
            data = {
                'timestamp': timestamp,
                'ip': ip,
                'uri': uri,
                'user_agent': user_agent,
            }
            querystring
            data.update(parse_qsl(querystring[1:], keep_blank_values=True))

            return data
        except:
            print(row)
            raise

