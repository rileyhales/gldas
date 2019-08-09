**********************
REST API Documentation
**********************

A REST API is a web service or a set of methods that can be used to produce or access data without a web interface.
REST APIs use the http protocol to request data.

Helper Functions
================

There are 4 help functions. Each return JSON objects containing information to assist in building a valid
timeseries request. The helpers are:

#. help
#. timeOptions
#. variableOptions
#. geometryOptions

Example
-------

.. code-block:: python

    import requests
    helpme = requests.get('[TethysPortalUrl]/apps/gldas/api/help/')
    time_opts = requests.get('[TethysPortalUrl]/apps/gldas/api/timeOptions/')
    var_opts = requests.get('[TethysPortalUrl]/apps/gldas/api/variableOptions/')
    geom_opts = requests.get('[TethysPortalUrl]/apps/gldas/api/geometryOptions/')

    print(helpme.text)


timeseries
==========

+--------------+---------------------------------------------------------------+-------------------+
| Parameter    | Description                                                   | Example           |
+==============+===============================================================+===================+
| time         | A 4 digit year, a decade, or 'alltimes'                       | '2019', '2010s'   |
+--------------+---------------------------------------------------------------+-------------------+
| variable     | The shortened name of a variable available in the GLDAS       | 'RootMoist_inst'  |
|              | datasets. (see variableOptions)                               |                   |
+--------------+---------------------------------------------------------------+-------------------+
|              | The kind of area for which to get a timeseries. The options   | 'Point',          |
| loc_type     | are at a point, within a bounding box (polygon), or within a  | 'Polygon',        |
|              | country/region                                                | 'VectorGeometry'  |
+--------------+---------------------------------------------------------------+-------------------+
|              | Required for Point or Polygon loc_type. For Point: a list     |                   |
| coords       | formatted as [lon, lat]. For Polygon: the list of the extents | [-110, 45]        |
|              | of the bounding box [minLon, maxLon, minLat, maxLat]          |                   |
+--------------+---------------------------------------------------------------+-------------------+
|              | Required for VectorGeometry loc_type. The name of one of the  |                   |
| region       | 25 UN Country Grouping Regions or the full, capitalized name  | 'Northern Africa' |
|              | of a country. Use geometryOptions for help.                   |                   |
+--------------+---------------------------------------------------------------+-------------------+

Example
-------

.. code-block:: python

    import requests
    parameters = {
        'time': '1990s',
        'variable': 'Tair_f_inst',
        'loc_type': 'VectorGeometry',
        'region': 'Italy',
    }
    italy_timeseries = requests.get('[TethysPortalUrl]/apps/gldas/api/timeseries/', params=parameters)
    print(italy_timeseries.text)
