from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .datatools import ts_plot
from .resources import gldas_variables
import ast, math, netCDF4, os      # ast can convert stringified json data back to a python dictionary

@login_required()
def generatePlot(request):
    """
    The controller for the ajax call to create a timeseries for the area chosen by the user's drawing
    """

    data = ast.literal_eval(request.body)
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

def getBounds(request):
    """
    Dynamically defines exact boundaries for the legend and wms so that they are synchronized
    Requires netcdf4, os, ast, math
    """

    data_dir = '/home/rchales/thredds/gldas/'

    data = ast.literal_eval(request.body)
    print data
    variable = data['variable']
    time = data['time']
    response_object = {}

    if time == 'alltimes':
        path = os.path.join(data_dir, 'raw')
        files = os.listdir(path)
        files.sort()
    else:
        path = os.path.join(data_dir, 'raw')
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