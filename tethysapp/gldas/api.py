from django.http import JsonResponse
# from rest_framework.decorators import api_view

from .options import gldas_variables, timeintervals, worldregions, countries
from .utilities import new_id, get_times
from .charts import newchart
from .app import Gldas as App


class TimeSeries:
    data = {}
    isValid = False
    error = None
    instance_id = new_id()

    def __init__(self, parameters):
        try:
            self.data['time'] = parameters['time']
            self.data['variable'] = parameters['variable']
            self.data['loc_type'] = parameters['loc_type']
            if self.data['loc_type'] == 'VectorGeometry':
                self.data['vectordata'] = parameters['vectordata']
            else:
                self.data['coords'] = parameters.getlist('coords')
        except KeyError as e:
            self.error = 'Missing parameter: ' + str(e).replace('"', '').replace("'", '')
        except Exception as e:
            return
        self.validate()

    # are the point coordinates valid
    def validate_points(self):
        test = self.data['coords']
        if type(test) is list and len(test) == 2:
            for i in test:
                try:
                    float(i)
                except Exception:
                    return False
            if not 180 > float(test[0]) > -180 and 90 > float(test[1]) > -90:
                return False
        else:
            return False
        return True

    # are the bounding box coordinates valid
    def validate_polygon(self):
        test = self.data['coords']
        if type(test) is list and len(test) == 4:
            for i in test:
                try:
                    float(i)
                except Exception:
                    return False
            if not float(test[1]) > float(test[0]) and float(test[3]) > float(test[2]):
                return False
            if not 180 > float(test[0]) > -180 and 180 > float(test[1]) > -180:
                return False
            if not 90 > float(test[2]) > -90 and 90 > float(test[3]) > -90:
                return False
        else:
            return False
        return True

    def validate(self):
        # check the 3 arguments are valid choices
        if not self.data['time'] in [i[1] for i in timeintervals()]:
            if not len(self.data['time']) == 4 and int(self.data['time']):
                self.error = 'Invalid time argument. Pick a year, decade, or "alltimes".'
        if not self.data['variable'] in [i[1] for i in gldas_variables()]:
            self.error = 'Invalid variable name. Use one of the shortened variables names given in variableOptions'
            return
        if not self.data['loc_type'] in ['Point', 'Polygon', 'VectorGeometry']:
            self.error = 'Invalid location type. Use only Point, Polygon, or VectorGeometry'
            return

        # perform validation for point
        if self.data['loc_type'] == 'Point':
            if not self.validate_points():
                self.error = 'Invalid coords argument, ask geometryOptions for more help'
                return

        # perform validation for polygon
        elif self.data['loc_type'] == 'Polygon':
            if self.validate_polygon():
                tmp = self.data['coords']
                self.data['coords'] = [[[tmp[0], tmp[2]], [tmp[0], tmp[3]], [tmp[1], tmp[3]], [tmp[1], tmp[2]]]]
            else:
                self.error = 'Invalid coords argument, ask geometryOptions for more help'
                return

        # perform validation for vectorgeometry
        elif self.data['loc_type'] == 'VectorGeometry':
            if self.data['vectordata'] in worldregions():
                self.data['vectordata'] = 'esri-regions-' + self.data['vectordata']
            elif self.data['vectordata'] in countries():
                self.data['vectordata'] = 'esri-countries-' + self.data['vectordata']
            else:
                self.error = 'Invalid vectordata, ' + self.data['vectordata'] + ' is not a valid region/country'
                return
        self.isValid = True
        return


# @api_view(['GET'])
def helpme(request):
    return JsonResponse({
        'api_methods': ['help', 'timeseries'],
        'help_url': App.githublink,
        'required_arguments': ['time', 'variable', 'loc_type', 'coords or vectordata'],
        'time': {
            'Description': 'A 4 digit year "YYYY", a decade "YYYYs", or "alltimes"',
            'Options': get_times(),
        },
        'variables': {
            'Description': 'The abbreviated name of a variable used by NASA in the GLDAS data files,',
            'Options': gldas_variables(),
        },
        'loc_type': 'The kind of area you want a timeseries for. Choose Point, Polygon (a Bounding Box), or '
                    'VectorGeometry (for countries/regions)',
        'vectordata': {
            'Description': 'Required if loc_type is VectorGeometry. Specify a region or country exactly as shown',
            'Regions': [i[0] for i in worldregions() if i[1] != '' and i[1] != 'none'],
            'Countries': countries(),
        },
        'coords': {
            'Description': 'Required if loc_type is Point or Polygon. A list of lat/long values.',
            'Point': 'A list: [longitude, latitude]',
            'Polygon': 'A list: [min_longitude, max_longitude, min_latitude, max_latitude]',
        }

    })


# @api_view(['GET'])
def timeseries(request):
    ts = TimeSeries(request.GET)
    if ts.isValid:
        return JsonResponse(newchart(ts.data))
    else:
        return JsonResponse({'Error': ts.error})
