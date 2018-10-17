from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .datatools import ts_plot
from . resources import gldas_variables
import ast      # ast can convert stringified json data back to a python dictionary

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