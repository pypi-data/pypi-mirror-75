from .api import API
from .endpoints import ObjectEndpoint, SubObjectEndpoint, DataEndpoint


class Model:
    pass


@API.register('areas', resource_name='areas', endpoint_type=ObjectEndpoint)
class Area(Model):
    def __init__(self, id: str, name: str, description: str, 
                 xlongitude: str, xlatitude: str, 
                 ylongitude: str, ylatitude: str):
        self.id = id
        self.name = name
        self.description = description
        self.xlongitude = xlongitude
        self.xlatitude = xlatitude
        self.ylongitude = ylongitude
        self.ylatitude = ylatitude


@API.register('sites', resource_name='sites', endpoint_type=ObjectEndpoint)
class Site(Model):
    def __init__(self, id: str, name: str, description: str, 
                 longitude: str, latitude: str, status: str):
        self.id = id
        self.name = name
        self.description = description
        self.longitude = longitude
        self.latitude = latitude
        self.status = status


@API.register('site_types', resource_name='sitetypes', 
              endpoint_type=SubObjectEndpoint, submodel=Site, sub_path='sites')
class SiteType(Model):
    def __init__(self, id: str, description: str):
        self.id = id
        self.description = description


class Report(list):
    pass

@API.register('daily_reports', resource_name='reports',
              endpoint_type=DataEndpoint, 
              required=['sites', 'start_date', 'end_date'],
              interval='daily', entry_point='Rows',
              paginate=True)
class DailyReport(Report):
    pass


@API.register('monthly_reports', resource_name='reports',
              endpoint_type=DataEndpoint, 
              required=['sites', 'start_date', 'end_date'],
              interval='monthly', entry_point='MonthCollection',
              paginate=True)
class MonthlyReport(Report):
    pass


@API.register('annual_reports', resource_name='reports',
              endpoint_type=DataEndpoint, 
              required=['sites', 'start_date', 'end_date'],
              interval='annual', entry_point='AnnualReportBody',
              paginate=True)
class AnnualReport(Report):
    pass


@API.register('daily_quality', resource_name='quality',
              endpoint_type=DataEndpoint, 
              required=['siteId', 'start_date', 'end_date'],
              interval='daily', entry_point='Qualities',
              paginate=False)
class DailyQuality(Report):
    pass


@API.register('overall_quality', resource_name='quality',
              endpoint_type=DataEndpoint, 
              required=['sites', 'start_date', 'end_date'],
              interval='overall', entry_point='data_quality',
              paginate=False)
class Quality(int):
    pass
