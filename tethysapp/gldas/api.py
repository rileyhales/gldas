from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from .datatools import validate_inputs, timeseries_plot
from .resources import gldas_variables


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def get_variables(request):
    """
    API Controller for getting a list of available variables
    """
    variables = gldas_variables()
    return JsonResponse(variables)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def tsPlotValues(data):
    """
    API controller for getting a list of plottable data at a point. Requires the same data dictionary as shown:
    data = {
        variable: short code name of the variable to be plotted
        type: Point or Rectangle
        coords: a list of coordinates [lat, lon]
    }
    """
    if validate_inputs(data):
        values = timeseries_plot(data)
    else:
        return JsonResponse({'Error': 'The data dictionary contains invalid information'})
    return JsonResponse({'values': values})
