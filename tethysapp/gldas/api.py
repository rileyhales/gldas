import datetime
import os

from django.http import JsonResponse
from rest_framework.decorators import api_view

from .options import gldas_variables, timeintervals
from .utilities import new_id
from .charts import newchart
from .app import Gldas as App

# todo return format option, which series to request?


# @api_view(['GET'])
def help(request):
    return JsonResponse({
        'api_calls': ['help', 'timeOptions', 'variableOptions', 'geometryOptions', 'timeseries'],
        'help_url': App.githublink,
        'required_arguments': {
            'time': '4 digit year, decade, alltimes  (see gldas/api/timeOptions for more help)',
            'variable': 'Short name of a GLDAS variable (see gldas/api/variableOptions for more help)',
            'loc_type': 'Point, Polygon, or VectorGeometry (see gldas/api/geometryOptions for more help)',
            'coords': 'REQUIRED IF loc_type is Point or Polygon (see gldas/api/geometryOptions for more help)',
            'region': 'REQUIRED IF loc_type is VectorGeometry (see gldas/api/geometryOptions for more help)',
        }
    })


# @api_view(['GET'])
def times(request):
    path = App.get_custom_setting('thredds_path')
    path = os.path.join(path, 'raw')
    files = os.listdir(path)
    files.sort()
    start = datetime.datetime.strptime(files[0], "GLDAS_NOAH025_M.A%Y%m.021.nc4").strftime("%B %Y")
    end = datetime.datetime.strptime(files[-1], "GLDAS_NOAH025_M.A%Y%m.021.nc4").strftime("%B %Y")
    dates = {
        'oldest_available': start,
        'newest_available': end,
        'decades': [i[1] for i in timeintervals()],
        'api_calls': 'A 4 digit year "YYYY", a decade "YYYYs", or "alltimes"',
    }
    return JsonResponse(dates)


# @api_view(['GET'])
def variables(request):
    return JsonResponse(gldas_variables())


# @api_view(['GET'])
def geometry(request):
    # todo geometry options list
    # describe coords for point/poly
    # list available countries/regions for vectorgeometry
    return


# @api_view(['GET'])
def timeseries(request):
    parameters = request.GET
    data = {}

    # use try/except to make data dictionary because we want to check that all params have been given
    try:
        data['time'] = parameters['time']
        data['variable'] = parameters['variable']
        data['coords'] = parameters.getlist('coords')
        data['loc_type'] = parameters['loc_type']

        if data['loc_type'] == 'VectorGeometry':
            data['region'] = parameters['region']
            data['instance_id'] = new_id()

    except KeyError as e:
        return JsonResponse({'Missing Parameter': str(e).replace('"', '').replace("'", '')})
    return JsonResponse(newchart(data))
