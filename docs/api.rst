**********************
REST API Documentation
**********************

A REST API is a web service or a set of methods that can be used to produce or access data without a web interface.
REST APIs use the http protocol to request data.

Helper Functions
================

There are 4 help functions. Each return JSON objects containing information to assist in building a valid
timeseries request. Each function requires no arguments and or authentication. The helpers are:

#. help
#. timeOptions
#. variableOptions
#. geometryOptions

Example
-------

.. code-block:: python

    import requests
    import json

    helpme = requests.get('[TethysPortalUrl]/apps/gldas/api/help/')
    time_opts = requests.get('[TethysPortalUrl]/apps/gldas/api/timeOptions/')
    var_opts = requests.get('[TethysPortalUrl]/apps/gldas/api/variableOptions/')
    geom_opts = requests.get('[TethysPortalUrl]/apps/gldas/api/geometryOptions/')

    print(helpme.text)
    help_as_dictionary = json.loads(helmp.text)


timeseries
==========

+------------+-------------------------------------------------------+-------------------+
| Parameter  | Description                                           | Example           |
+============+=======================================================+===================+
| time       | A 4 digit year, a decade, or 'alltimes'               | - '2019'          |
|            |                                                       | - '2010s'         |
+------------+-------------------------------------------------------+-------------------+
| variable   | The shortened name of a variable available in the     | 'RootMoist_inst'  |
|            | GLDAS datasets. (see variableOptions)                 |                   |
+------------+-------------------------------------------------------+-------------------+
|            | The kind of area for which to get a timeseries. The   | - 'Point'         |
| loc_type   | options are at a point, within a bounding box         | - 'Polygon'       |
|            | (polygon), or country/region                          | - 'VectorGeometry'|
+------------+-------------------------------------------------------+-------------------+
|            | Required for Point or Polygon loc_type. For Point: a  |                   |
| coords     | list formatted as [lon, lat]. For Polygon: the list   | [-110, 45]        |
|            | of the extents of the bounding box [minLon, maxLon,   |                   |
|            | minLat, maxLat]                                       |                   |
+------------+-------------------------------------------------------+-------------------+
|            | Required for VectorGeometry loc_type. The name of one |                   |
| region     | of the 25 UN Country Grouping Regions or the full,    | 'Northern Africa' |
|            | capitalized name of a country.                        |                   |
+------------+-------------------------------------------------------+-------------------+

Example
-------

.. code-block:: python

    import requests
    import json

    parameters = {
        'time': '1990s',
        'variable': 'Tair_f_inst',
        'loc_type': 'VectorGeometry',
        'region': 'Italy',
    }
    italy_timeseries = requests.get('[TethysPortalUrl]/apps/gldas/api/timeseries/', params=parameters)

    italy_timeseries_as_dictionary = json.loads(italy_timeseries.text)
