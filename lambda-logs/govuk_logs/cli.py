import gzip
from os.path import dirname
from os import makedirs

from .base import Base


class Cli(Base):

    def open_for_read(self):
        return gzip.open(self.filename, 'rt')


    def open_for_write(self, path):
        makedirs(dirname(path), exist_ok=True)
        return gzip.open(path, 'wt')
