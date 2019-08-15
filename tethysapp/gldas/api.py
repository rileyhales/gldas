from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from .options import gldas_variables, timeintervals, worldregions, countries
from .utilities import new_id, get_times
from .charts import newchart
from .app import Gldas as App


class TimeSeries:
    data = {}
    isValid = False
    error = None

    def __init__(self, parameters):
        try:
            self.data['time'] = parameters['time']
            self.data['variable'] = parameters['variable']
            self.data['location'] = parameters.getlist('location')
        except KeyError as e:
            self.error = 'Missing parameter: ' + str(e).replace('"', '').replace("'", '')
        except Exception as e:
            self.error = e
        else:
            if 'stats' in dict(parameters):
                self.data['stats'] = parameters['stats']
            else:
                self.data['stats'] = False
            self.validate()

    # are the point coordinates valid
    def validate_points(self):
        tmp = self.data['location']
        for i in tmp:
            try:
                float(i)
            except ValueError:
                return False
        if not 180 > float(tmp[0]) > -180 and 90 > float(tmp[1]) > -90:
            return False
        self.data['coords'] = self.data['location']
        return True

    # are the bounding box coordinates valid
    def validate_polygon(self):
        tmp = self.data['location']
        for i in tmp:
            try:
                float(i)
            except ValueError:
                return False
        if not float(tmp[1]) > float(tmp[0]) and float(tmp[3]) > float(tmp[2]):
            return False
        if not 180 > float(tmp[0]) > -180 and 180 > float(tmp[1]) > -180:
            return False
        if not 90 > float(tmp[2]) > -90 and 90 > float(tmp[3]) > -90:
            return False
        self.data['coords'] = [[[tmp[0], tmp[2]], [tmp[0], tmp[3]], [tmp[1], tmp[3]], [tmp[1], tmp[2]]]]
        return True

    def validate(self):
        # validate time argument
        if not self.data['time'] in [i[1] for i in timeintervals()]:
            self.data['stats'] = False
            if not len(self.data['time']) == 4 and int(self.data['time']):
                self.error = 'Invalid time argument. Pick a year, decade, or "alltimes".'

        # validate variable argument
        if not self.data['variable'] in [i[1] for i in gldas_variables()]:
            self.error = 'Invalid variable name. Use one of the shortened variables names given in variableOptions'
            return

        # validate location argument
        if len(self.data['location']) == 1:
            self.data['loc_type'] = 'VectorGeometry'
            self.data['location'] = self.data['location'][0]
            if self.data['location'] in worldregions():
                self.data['vectordata'] = 'esri-regions-' + self.data['location']
            elif self.data['location'] in countries():
                self.data['vectordata'] = 'esri-countries-' + self.data['location']
            else:
                self.error = 'Country/Region name not recognized. Check your spelling/capitalization'
                return
        elif len(self.data['location']) == 2:
            self.data['loc_type'] = 'Point'
            if not self.validate_points():
                self.error = 'Invalid list of coordinates for a Point location.'
                return
        elif len(self.data['location']) == 4:
            self.data['loc_type'] = 'Polygon'
            if not self.validate_polygon():
                self.error = 'Invalid list of coordinates for a Bounding Box location.'
                return
        else:
            self.error = 'Invalid location. Enter a list of valid coordinates or a country/region name'
            return

        # all arguments pass the tests
        self.isValid = True
        self.data['instance_id'] = new_id()
        return


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def helpme(request):
    return JsonResponse({
        'documentation_website': App.docslink,
        'required_arguments': ['time', 'variable', 'location'],
        'time': {
            'Description': 'A 4 digit year "YYYY", a decade "YYYYs", or "alltimes"',
            'Options': get_times(),
        },
        'variable': {
            'Description': 'The abbreviated name of a variable used by NASA in the GLDAS data files',
            'Options': gldas_variables(),
        },
        'location': {
            'Description': 'Available locations are points, bounding boxes, countries, or world regions',
            'Point': 'To get values at a point, provide a list in the form: [longitude, latitude]',
            'Bounding Box': 'To get values in a bounding box, provide a list in the form: '
                            '[min_longitude, max_longitude, min_latitude, max_latitude]',
            'Regions': [i[0] for i in worldregions() if i[1] != '' and i[1] != 'none'],
            'Countries': countries(),
        },
    })


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def timeseries(request):
    ts = TimeSeries(request.GET)
    if ts.isValid:
        return JsonResponse(newchart(ts.data))
    else:
        return JsonResponse({'Error': ts.error})
