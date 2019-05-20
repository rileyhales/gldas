from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from .options import gldas_variables, timecoverage

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def gldasvariables(request):
    """
    API Controller for getting a list of available variables
    Dependencies: gldas_variables (model)
    """
    return JsonResponse(gldas_variables())


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def timecoverage(request):
    """
    API Controller for getting a list of available times
    timecoverage (model)
    """
    return JsonResponse(timecoverage())
