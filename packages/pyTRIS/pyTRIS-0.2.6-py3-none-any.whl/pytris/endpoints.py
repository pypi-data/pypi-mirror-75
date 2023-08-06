from typing import Iterator, Optional, Type, Union

from .base_models import Model, Report
from .parameters import Parameter
from .requests import HTTPRequest


class BaseEndpoint:
    def __init__(self, version: str, path: str, 
                 model: Union[Type[Model], Type[Report]], 
                 request_class: Type[HTTPRequest]):
        self.version = version
        self.path = path
        self.model = model
        self.request_class = request_class

    def all(self, *args, **kwargs):
        raise NotImplementedError('Not implemented for this endpoint')

    def get(self, *args, **kwargs):
        raise NotImplementedError('Not implemented for this endpoint')


class ObjectEndpoint(BaseEndpoint):
    def all(self):
        request = self.request_class(self.version, self.path)
        return self._objects_from_resp(request.fetch(), self.model, self.path)

    def get(self, key: Union[int, str]):
        # TODO check key type
        item_path = '/'.join([self.path, str(key)])
        request = self.request_class(self.version, item_path)

        # Single item endpoints seem to still return an iterable for objects.
        # Only return the first one.
        return next(
            self._objects_from_resp(request.fetch(), self.model, self.path)
        )
    
    @staticmethod
    def _objects_from_resp(resp: dict, model: Union[Type[Model], Type[Report]], 
                           key_name: str):
        return (
            model(**{k.lower(): v for k, v in mod_dict.items()})
            for mod_dict in resp[key_name]
        )

class SubObjectEndpoint(ObjectEndpoint):
    def __init__(self, version: str, path: str, 
                 model: Type[Model], submodel: Type[Model], 
                 sub_path: str, request_class: Type[HTTPRequest]):
        super().__init__(version, path, model, request_class)
        self.submodel = submodel
        self.sub_path = sub_path

    def get(self, *args, **kwargs):
        BaseEndpoint.get(self, *args, **kwargs)
    
    def get_children(self, key: Union[int, str]):
        item_path = '/'.join([self.path, str(key), self.sub_path])
        request = self.request_class(self.version, item_path)
        return self._objects_from_resp(
            request.fetch(), self.submodel, self.sub_path
        )


class DataEndpoint(BaseEndpoint):
    PAGE_SIZE = 200

    def __init__(self, version: str, path: str, 
                 model: Type[Report], request_class: Type[HTTPRequest], 
                 interval: str, entry_point: str, 
                 parameters: Iterator[Type[Parameter]], paginate: bool):
        super().__init__(version, path, model, request_class)
        self._interval = interval
        self._entry_point = entry_point
        self._paginate = paginate
        self._parameters = parameters

    def get(self, page_size: Optional[int] = None, **kwargs):
        if not page_size:
            page_size = self.PAGE_SIZE

        # Check if we're missing any of the required parameters
        missing_params = [
            k.name for k in self._parameters 
            if k.required and k.name not in kwargs.keys()
        ]

        if missing_params:
            raise ValueError(
                f'Missing required parameters: {", ".join(missing_params)}'
            )
        
        param_dict = dict()

        if self._paginate:
            param_dict['page'] = 1
            param_dict['page_size'] = page_size
        
        for param in self._parameters:
            param_dict[param.name] = param.to_value(kwargs[param.name])

        endpoint_path = '/'.join([self.path, self._interval])

        request = self.request_class(self.version, endpoint_path)
        resp = request.fetch(params=param_dict)

        results = resp[self._entry_point]

        # TODO make this neater? It's kinda ugly.
        if self._paginate:
            next_page = self._next_page_link(resp)
            while next_page is not None:
                param_dict['page'] += 1
                resp = request.fetch(params=param_dict)

                results += resp[self._entry_point]
                next_page = self._next_page_link(resp)
        
        return self.model(results)
                
    
    @staticmethod
    def _next_page_link(resp: dict):
        header = resp.get('Header', dict())
        links = header.get('links', [])

        for link in links:
            if link['rel'].lower() == 'nextpage':
                return link['href']
        
        return None
