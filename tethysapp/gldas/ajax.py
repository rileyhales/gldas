from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required()
def generatePlot(request):
    """
    The controller for the ajax call to create a timeseries for the area chosen by the user's drawing
    """
    from .model import gldas_variables
    from .tools import ts_plot
    import ast

    data = ast.literal_eval(request.body.decode('utf-8'))
    response_object = {}
    plot_items = ts_plot(data)
    response_object['units'] = plot_items[0]
    response_object['values'] = plot_items[1]
    variables = gldas_variables()
    for key in variables:
        if variables[key] == data['variable']:
            name = key
            break
    response_object['name'] = name
    return JsonResponse(response_object)


@login_required()
def getBounds(request):
    """
    Dynamically defines exact boundaries for the legend and wms so that they are synchronized
    This was substituted for statically defined values to improve performance on the most common values.
    Will be reimplemented when the app supports custom time values
    Requires netcdf4, os, ast, math
    """
    from .model import app_configuration
    import ast
    import math
    import netCDF4
    import os

    configs = app_configuration()
    thredds_data_dir = configs['thredds_data_dir']

    data = ast.literal_eval(request.body)
    variable = data['variable']
    time = data['time']
    response_object = {}

    if time == 'alltimes':
        path = os.path.join(thredds_data_dir, 'raw')
        files = os.listdir(path)
        files.sort()
    else:
        path = os.path.join(thredds_data_dir, 'raw')
        allfiles = os.listdir(path)
        files = [nc for nc in allfiles if nc.startswith("GLDAS_NOAH025_M.A" + str(time))]
        files.sort()

    minimum = 1000000
    maximum = -1000000
    for nc in files:
        dataset = netCDF4.Dataset(path + '/' + nc, 'r')
        data_dict = dataset[variable].__dict__
        if data_dict['vmax'] > maximum:
            maximum = data_dict['vmax']
        if data_dict['vmin'] < minimum:
            minimum = data_dict['vmin']

    response_object['minimum'] = math.floor(minimum)
    response_object['maximum'] = math.ceil(maximum)

    return JsonResponse(response_object)


@login_required()
def customsettings(request):
    """
    returns the paths to the data/thredds services taken from the custom settings and gives it to the javascript
    """
    from .model import app_configuration
    return JsonResponse(app_configuration())
