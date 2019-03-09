from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from .tools import ts_plot
from .model import gldas_variables, get_times
import ast

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def get_variables(request):
    """
    API Controller for getting a list of available variables
    .resources gldas_variables
    """
    variables = gldas_variables()
    return JsonResponse(variables)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def tsPlotValues(request):
    """
    API controller for getting a list of plottable data at a point. Requires the same data dictionary as shown:
    data = {
        variable: short code name of the variable to be plotted
        type: Point or Rectangle
        coords: a list of coordinates [lat, lon]
    }
    Dependencies:
        ast: to decode the request that contains the dictionary
        .resources ts_plot
    """
    data = ast.literal_eval(request.body)
    response_object = {}
    response_object['values'] = ts_plot(data)
    return JsonResponse(response_object)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def getTimes(request):
    """
    API Controller for getting a list of available times
    .resources get_times
    """
    times = get_times()
    return JsonResponse(times)