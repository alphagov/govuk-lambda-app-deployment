import re


class Base(object):

    def __init__(self, filename):
        self.filename = filename

    def open_for_read(self):
        raise NotImplementedError

    def open_for_write(self, path):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError

    def transform_row(self, row):
        try:
            timestamp, status, file_downloaded, ip, referrer, user_agent, ga_client_id = row
            if re.search('https://www.gov.uk/', referrer) is None:
                return {
                    'timestamp': timestamp,
                    'status': status,
                    'file_downloaded': file_downloaded,
                    'ip': ip,
                    'referrer': referrer,
                    'user_agent': user_agent,
                    'ga_client_id': ga_client_id
                }
            else:
                return ""
        except:
            print(row)
            raise
