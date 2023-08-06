from typing import Type
import warnings

from .endpoints import BaseEndpoint
from .errors import UnknownVersionWarning
from .requests import HTTPRequest


KNOWN_VERSIONS = ['1.0']

class API:
    """Main entry point for accessing the webTRIS API.
    """
    def __init__(self, version: str = '1.0',
                 request_class: Type[HTTPRequest] = HTTPRequest):
        """Constructor for the API object.

        Args:
            version (str, optional): 
                The version of the webTRIS API to be used. Defaults to '1.0'.
            request_class (Type[HTTPRequest], optional): 
                The class for processing responses from the API. Defaults to 
                HTTPRequest.
        """
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
    def register(cls, name: str, resource_name: str, 
                 endpoint_type: Type[BaseEndpoint], **kwargs):
        """Class method for registering a model with the API.

        This method should **only** be used by module developers - it allows for
        the addition of new resources for access through the API.

        Args:
            name (str): 
                The name of the method to be registered with the api. This 
                should ideally consist solely of letters and underscores.
            resource_name (str): 
                The name of the resource to be accessed.
            endpoint_type (Type[BaseEndpoint]): 
                The class of Endpoint to be used for accessing the data.
            **kwargs:
                Any additional keyword arguments required by the Endpoint 
                chosen.
        """
        def decorator(model):
            def accessor(self):
                return endpoint_type(
                    version=self.version, path=resource_name, 
                    model=model, request_class=self._request_class, **kwargs
                )

            doc = (
                f'Method for accessing endpoints for {model.__name__} resources'
            )

            if 'parameters' in kwargs.keys():
                required = ', '.join(
                    param.name for param in kwargs['parameters'] 
                    if param.required
                )
                doc += f'\n\nRequired parameters for endpoints: {required}'
                    
            accessor.__name__ = name
            accessor.__doc__ = doc
            setattr(cls, name, accessor)
            return model
        return decorator
