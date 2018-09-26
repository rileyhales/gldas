from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .datatools import timeseries_plot
import ast      # ast can convert stringified json data back to a python dictionary

@login_required()
def generatePlot(request):
    """
    The controller for the ajax call to create a timeseries for the area chosen by the user's drawing
    """
    print(request)
    data = ast.literal_eval(request.body)
    response_object = {}
    response_object['values'] = timeseries_plot(data)
    print(response_object)
    return JsonResponse(response_object)