**********************
REST API Documentation
**********************

A REST API is a web service or a set of methods that can be used to produce or access data without a web interface.
REST APIs use the http protocol to request data.

help
====

The help function requires no arguments and returns a JSON object. The response contains information about each of the
parameters for the timeseries function and links to help websites.

.. code-block:: python

    import requests
    import json

    helpme = requests.get('[TethysPortalUrl]/apps/gldas/api/help/')

    print(helpme.text)
    help_as_dictionary = json.loads(helmp.text)

timeseries
==========

+------------+--------------------------------------------------+--------------------------+
| Parameter  | Description                                      | Examples                 |
+============+==================================================+==========================+
| time       | A 4 digit year, a decade, or 'alltimes'          | - '2019'                 |
|            |                                                  | - '2010s'                |
|            |                                                  | - 'alltimes'             |
+------------+--------------------------------------------------+--------------------------+
| variable   | The shortened name of a GLDAS variable           | 'RootMoist_inst'         |
+------------+--------------------------------------------------+--------------------------+
|            | - The name of a country or UN world region       | - 'Northern Africa'      |
| location   | - (Point) [longitude, latitude]                  | - [-110, 45]             |
|            | - (Bound Box) [minLon, maxLon, minLat, maxLat]   | - [-115, -105, 40, 50]   |
+------------+--------------------------------------------------+--------------------------+
| stats      | Generates the statistical summaries              | - True                   |
| (optional) |                                                  | - False (default)        |
+------------+--------------------------------------------------+--------------------------+

.. code-block:: python

    import requests
    import json

    parameters = {
        'time': '1990s',
        'variable': 'Tair_f_inst',
        'location': 'Italy',
    }
    italy_timeseries = requests.get('[TethysPortalUrl]/apps/gldas/api/timeseries/', params=parameters)

    italy_timeseries_as_dictionary = json.loads(italy_timeseries.text)
