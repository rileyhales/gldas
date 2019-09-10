======================
Install the Tethys App
======================
Please refer to the `Tethys Documentation <http://docs.tethysplatform.org/en/stable/>`_ for help installing Tethys.

Clone from Git and install
--------------------------
This application is compatible with Tethys 2.X and Tethys 3 Distributions and as such is compatible with both Python 2
and 3 and Django 1 and 2. Install the latest version of Tethys before installing this app. This app requires the python
packages:

* numpy
* pandas
* netcdf4
* rasterio
* rasterstats
* pyshp
* json
* statistics

On the terminal of the server where you're installing the app:

.. code-block:: bash

    conda activate tethys
    cd /path/to/apps/directory/

    git clone https://github.com/rileyhales/gldas.git
    cd gldas

    # for tethys 3
    tethys install

    # for tethys 2
    python setup.py develop
    tethys manage collectstatic

Reset the server, then attempt to log in through the web interface as an administrator. The app should appear in the
Apps Library page in grey indicating you need to configure the custom settings.

Create a THREDDS Data Server
----------------------------
Refer to the documentation for THREDDS to set up an instance of on your tethys server (a UNIDATA has containerized
THREDDS and tethys offers commands to init a container). You will need to modify Thredds' settings files to enable WMS
services and support for netCDF files on your server. In the folder where you installed Thredds, there should be a file
called ``catalog.xml``.

.. code-block:: bash

    vim catalog.xml

At the top of the document is a list of supported services. Make sure the line for wms is not commented out.

| ``<service name="wms" serviceType="WMS" base="/thredds/wms/" />``

Scroll down toward the end of the section that says ``filter``. This is the section that limits which kinds of datasets Thredds will process. We need it to accept .nc, .nc4, and .ncml file types. Make sure your ``filter`` tag includes the following lines.

.. code-block:: xml

    <filter>
        <include wildcard="*.nc4"/>
        <include wildcard="*.ncml"/>
    </filter>

.. code-block:: bash

    vim threddsConfig.xml

Find the section near the top about CORS (Cross-Origin Resource Sharing). CORS allows Thredds to serve data to servers besides the host where it is located. Depending on your exact setup, you need to enable CORS by uncommenting these tags.

.. code-block:: xml

    <CORS>
        <enabled>true</enabled>
        <maxAge>1728000</maxAge>
        <allowedMethods>GET</allowedMethods>
        <allowedHeaders>Authorization</allowedHeaders>
        <allowedOrigin>``</allowedOrigin>
    </CORS>

Reset the Thredds server so the catalog is regenerated with the edits that you've made. The command to reset your
server will vary based on your installation method, such as ``docker restart thredds`` or
``sudo systemctl reset tomcat``.


GLDAS Downloads
---------------
In THREDDS' public folder, where your datasets are stored,
create a new folder called ``gldas``. Get the path to this directory (pwd) and save it for later. You need to fill this
folder with the GLDAS data from NASA and there are 2 ways to do this.

1. Run the gldasworkflow.sh workflow found in the gldasworkflow folder of the app using the path to the ``gldas`` folder
   as the argument to the function.
2. Go to `disc.gsfc.nasa.gov <https://disc.gsfc.nasa.gov/datasets?keywords=gldas>`_ and sign up for an Earth Data
   account. Download all the GLDAS 2 and 2.1 monthly, 1/4 degree resolution netcdf datasets. Create a directory inside
   the ``gldas`` folder called ``raw`` and save all the data here. Copy the contents of ``gldasworkflow/ncml`` directory
   to the ``gldas`` directory.

If you did it correctly, your folder should look like this:

| gldas
| --->1950s.ncml
| --->1960s.ncml
| --->1970s.ncml
| --->1980s.ncml
| --->1990s.ncml
| --->2000s.ncml
| --->2010s.ncml
| --->alltimes.ncml
| --->raw (directory)
|     ---><all the gldas datasets here>

Create a GeoServer
------------------
Refer to the documentation for GeoServer to set up an instance of GeoServer on your tethys server. There is an official
GeoServer container which you can install using tethys commands. Log in to your tethys portal as an administrator and
create a Spatial Dataset Service Setting configured to the GeoServer instance you just created.

If you choose not to use geoserver, your users will not be able to view custom shapefiles in the app.

Specify Custom Settings
-----------------------
Log in to your Tethys portal as an admin. Click on the grey GLDAS box and specify these settings:

* ``thredds_path:`` This is the full path to the directory named gldas that you should have created within the thredds data directory during step 2. You can get this by navigating to that folder in the terminal and then using the ``pwd`` command. (example: ``/tomcat/content/thredds/gldas/``)
* ``thredds_url:`` This is the base URL to Thredds WMS services that the app uses to build urls for each of the WMS layers generated for the netcdf datasets. If you followed the typical configuration of thredds (these instructions) then your base url will look something like ``yourserver.com/thredds/wms/testAll/gldas/``. You can verify this by opening the thredds catalog in a web browser (typically at ``yourserver.com/thredds/catalog.html``). Navigate to one of the GLDAS netcdf files and click the WMS link. A page showing an xml document should load. Copy the url in the address bar until you get to the ``/gldas/`` folder in that url. Do not include ``/raw/name_of_dataset.nc`` or the request that comes after. (example: ``https://tethys.byu.edu/thredds/wms/testAll/gldas/``)
* ``Spatial Dataset Services:`` Create a Tethys SpatialDatasetService configured with the correct urls and admin username/password for the GeoServer from step 3
