import json
from typing import Optional
from urllib.parse import urljoin, urlencode
from urllib.request import urlopen

from .errors import DataUnavailableError


class HTTPRequest:
    BASE_URL = 'http://webtris.highwaysengland.co.uk/api/v{version}/'

    def __init__(self, version: str, path: str):
        self.version = version
        self.path = path

    @property
    def url(self):
        return urljoin(self.BASE_URL.format(version=self.version), self.path)

    def fetch(self, params: Optional[dict] = None):
        if params is not None:
            data = urlencode(params)
            url = self.url + f'?{data}'
        else:
            url = self.url
        print(f"Requesting {url}")
        resp = urlopen(url)

        data = resp.read()
        if data:
            return json.loads(data)
        else:
            raise DataUnavailableError('No data found.')
