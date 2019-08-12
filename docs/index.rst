GLDAS Data Tool
===============
The GLDAS Data Tool is a tool to facilitate downloading, visualizing, processing, analyzing, and sharing GLDAS v2.X
data from the NASA. GLDAS, Global Land Data Assimilation System, is a historical earth observation dataset based on the
LIS, Land Information System, land-surface model.

The tool is a Tethys application with scripts for automated install and data downloads, several tools for data
visualization through maps and charts, and a REST API for programmatic access to the data. Tethys Platform is an
open-source software developed at Brigham Young University in the Hydroinformatics Lab. Tethys makes it easier to
develop and deploy web-apps for scientific data, especially geospatial and water resources related datasets.
`Read the Documentation for Tethys <http://docs.tethysplatform.org/en/stable/>`_ and visit the
`GitHub repository <https://github.com/tethysplatform/tethys>`_.

Improvements Over GIOVANNI
--------------------------
* Access app functions through a REST API
* Built entirely on OGC web services
* Extendable framework for other netCDF Earth Observation data and applications
* Faster and more interactive animated maps
* Better timeseries generating capabilities
* More options for regions to get timeseries including user-submitted shapefiles
* Functions can be run as python scripts outside of Tethys

References
----------
Some references for GLDAS and related NASA projects:

* Download GLDAS data: `<https://daac.gsfc.nasa.gov/datasets?keywords=gldas>`_
* GIOVANNI Data Viewer: `<https://giovanni.gsfc.nasa.gov/giovanni/>`_
* NASA LDAS Program: `<https://ldas.gsfc.nasa.gov/gldas/>`_
* NASA LIS (Land Information System): `<https://lis.gsfc.nasa.gov/>`_
* NASA EOS (Earth Observing System): `<https://eospso.nasa.gov/>`_
* NEO (NASA Earth Observations): `<https://neo.sci.gsfc.nasa.gov/>`_

.. toctree::
    :caption: Table of Contents
    :name: mastertoc

    workshop
    api
    license
