import datetime
import os

from django.http import JsonResponse
from rest_framework.decorators import api_view

from .options import gldas_variables
from .charts import newchart
from .app import Gldas as App


@api_view(['GET'])
def getcapabilities(request):
    return JsonResponse({
        'api_calls': ['getcapabilities', 'eodatamodels', 'gldasvariables', 'gldasdates', 'timeseries']
    })


@api_view(['GET'])
def gldasdates(request):
    path = App.get_custom_setting('thredds_path')
    path = os.path.join(path, 'raw')
    files = os.listdir(path)
    files.sort()
    start = datetime.datetime.strptime(files[0], "GLDAS_NOAH025_M.A%Y%m.021.nc4").strftime("%B %Y")
    end = datetime.datetime.strptime(files[-1], "GLDAS_NOAH025_M.A%Y%m.021.nc4").strftime("%B %Y")
    dates = {
        'start': start,
        'end': end,
        'api_calls': 'Provide a string type 4 digit year or "alltimes"',
    }
    return JsonResponse(dates)


@api_view(['GET'])
def gldasvariables(request):
    return JsonResponse(gldas_variables())


@api_view(['GET'])
def timeseries(request):
    parameters = request.GET
    data = {}

    # use try/except to make data dictionary because we want to check that all params have been given
    try:
        data['variable'] = parameters['variable']
        data['coords'] = parameters.getlist('coords')
        data['loc_type'] = parameters['loc_type']
        data['time'] = parameters['time']

        if data['loc_type'] == 'Shapefile':
            data['region'] = parameters['region']

    except KeyError as e:
        return JsonResponse({'Missing Parameter': str(e).replace('"', '').replace("'", '')})
    return JsonResponse(newchart(data))
