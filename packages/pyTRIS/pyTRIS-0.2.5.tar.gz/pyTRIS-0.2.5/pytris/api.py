import json
from urllib.parse import urljoin 
from urllib.request import urlopen
import warnings

from .errors import UnknownVersionWarning
from .requests import HTTPRequest


KNOWN_VERSIONS = ['1.0']

class API:
    def __init__(self, version: str, request_class=HTTPRequest):
        if version not in KNOWN_VERSIONS:
            warnings.warn(
                f'API version "{version}" has not been tested with these '
                f'methods. Performance cannot be guaranteed (known versions: '
                f'{",".join(KNOWN_VERSIONS)})',
                UnknownVersionWarning, stacklevel=2
            )
        self.version = version
        self._request_class = request_class

    @classmethod
    def register(cls, name, resource_name, endpoint_type, **kwargs):
        def decorator(model):
            def accessor(self):
                return endpoint_type(
                    version=self.version, path=resource_name, 
                    model=model, request_class=self._request_class, **kwargs
                )
            accessor.__name__ = name
            accessor.__doc__ = 'Endpoint for {}s'.format(model.__name__)
            setattr(cls, name, accessor)
            return model
        return decorator
