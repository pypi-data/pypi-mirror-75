class BaseEndpoint:
    def __init__(self, version, path, model, request_class):
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

    def get(self, key):
        # TODO check key type
        item_path = '/'.join([self.path, str(key)])
        request = self.request_class(self.version, item_path)

        # Single item endpoints seem to still return an iterable for objects.
        # Only return the first one.
        return next(
            self._objects_from_resp(request.fetch(), self.model, self.path)
        )
    
    def _objects_from_resp(self, resp, model, key_name):
        return (
            model(**{k.lower(): v for k, v in mod_dict.items()})
            for mod_dict in resp[key_name]
        )

class SubObjectEndpoint(ObjectEndpoint):
    def __init__(self, version, path, model, submodel, sub_path, request_class):
        super().__init__(version, path, model, request_class)
        self.submodel = submodel
        self.sub_path = sub_path

    def get(self, *args, **kwargs):
        BaseEndpoint.get(self, *args, **kwargs)
    
    def get_children(self, key):
        item_path = '/'.join([self.path, str(key), self.sub_path])
        request = self.request_class(self.version, item_path)
        return self._objects_from_resp(
            request.fetch(), self.submodel, self.sub_path
        )


class DataEndpoint(BaseEndpoint):
    PAGE_SIZE = 50

    def __init__(self, version, path, model, request_class, interval, 
                 entry_point, required, paginate):
        super().__init__(version, path, model, request_class)
        self._interval = interval
        self._entry_point = entry_point
        self._paginate = paginate
        self._required = required

    def get(self, page_size=None, **kwargs):
        if not page_size:
            page_size = self.PAGE_SIZE
        if not all(c in kwargs.keys() for c in self._required):
            raise ValueError
        
        if self._paginate:
            kwargs['page'] = 1
            kwargs['page_size'] = page_size

        endpoint_path = '/'.join([self.path, self._interval])

        request = self.request_class(self.version, endpoint_path)
        resp = request.fetch(params=kwargs)

        results = resp[self._entry_point]

        # TODO make this neater? It's kinda ugly.
        if self._paginate:
            next_page = self._next_page_link(resp)
            while next_page is not None:
                kwargs['page'] += 1
                resp = request.fetch(params=kwargs)

                results += resp[self._entry_point]
                next_page = self._next_page_link(resp)
        
        return self.model(results)
                
    
    @staticmethod
    def _next_page_link(resp):
        header = resp.get('Header', dict())
        links = header.get('links', [])

        for link in links:
            if link['rel'].lower() == 'nextpage':
                return link['href']
        
        return None