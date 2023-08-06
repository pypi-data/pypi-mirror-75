from .api import API
from .base_models import Model, Report
from .endpoints import ObjectEndpoint, SubObjectEndpoint, DataEndpoint
from .parameters import Parameter, DateParameter
from .utilities import requires_pandas


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


@API.register('daily_reports', resource_name='reports',
              endpoint_type=DataEndpoint, 
              parameters=[
                  Parameter('sites', required=True), 
                  DateParameter('start_date', required=True), 
                  DateParameter('end_date', required=True),
              ],
              interval='daily', entry_point='Rows',
              paginate=True)
class DailyReport(Report):
    pass


@API.register('monthly_reports', resource_name='reports',
              endpoint_type=DataEndpoint, 
              parameters=[
                  Parameter('sites', required=True), 
                  DateParameter('start_date', required=True), 
                  DateParameter('end_date', required=True),
              ],
              interval='monthly', entry_point='MonthCollection',
              paginate=True)
class MonthlyReport(Report):
    @requires_pandas
    def to_frame(self):
        from copy import deepcopy

        dupe = deepcopy(self)
        frames = dict()

        for col in ('Days', 'Daily Aggregations', 'Hourly Aggregations'):
            frames[col] = json_normalize(dupe, col, meta=['Month', 'SiteId'])
            for m in dupe:
                m.pop(col)

        last = json_normalize(dupe)
        last.columns = [
            c.replace('Summary Aggregations.', '') for c in last.columns
        ]
        frames['Summary Aggregations'] = last

        del dupe

        return frames


@API.register('annual_reports', resource_name='reports',
              endpoint_type=DataEndpoint, 
              parameters=[
                  Parameter('sites', required=True), 
                  DateParameter('start_date', required=True), 
                  DateParameter('end_date', required=True),
              ],
              interval='annual', entry_point='AnnualReportBody',
              paginate=True)
class AnnualReport(Report):
    @requires_pandas
    def to_frame(self):
        res = json_normalize(
            self, 'AnnualReportMonthlyDataRows', meta=['Year', 'SiteId']
        )

        res.columns = [c.replace('AnnualReportRow.', '') for c in res.columns]
        return res


@API.register('daily_quality', resource_name='quality',
              endpoint_type=DataEndpoint, 
              parameters=[
                  Parameter('siteId', required=True), 
                  DateParameter('start_date', required=True), 
                  DateParameter('end_date', required=True),
              ],
              interval='daily', entry_point='Qualities',
              paginate=False)
class DailyQuality(Report):
    pass


@API.register('overall_quality', resource_name='quality',
              endpoint_type=DataEndpoint, 
              parameters=[
                  Parameter('sites', required=True), 
                  DateParameter('start_date', required=True), 
                  DateParameter('end_date', required=True),
              ],
              interval='overall', entry_point='data_quality',
              paginate=False)
class Quality(int):
    pass
