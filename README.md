# GLDAS Data Tool Documentation
[![Documentation Status](https://readthedocs.org/projects/gldas-data-tool/badge/?version=latest)](https://gldas-data-tool.readthedocs.io/en/latest/?badge=latest)
   
This is a Tethys 2/3 compatible app that visualizes data from the NASA GES Disc website. It was developed to show ¼ degree resolution netcdf4 (.nc4) datasets with monthly averages. Datasets of other resolutions and for other time-periods may also work.

© Riley Hales, 2019. Developed at the BYU Hydroinformatics Lab.

## App Features
1. View time-animated maps of all GLDAS variables.
2. View world region boundaries and any country boundaries.
3. Upload a polygon shapefile to view on the map and use it to generate timeseries.
4. Customize color scheme, opacity, animation/playback speed, toggle on/off, time period, etc of all spatial data.
5. View the Latitude/Longitude Coordinates of anywhere on the planet by hovering your mouse over the map.
6. Generate timeseries by drawing Points/Bounding Boxes on the map, uploading a polygon shapefile, or choosing a world region or country boundary.
7. Plot the timeseries on 5 different charts including timeseries and simple statistical analysis.
8. Export timeseries data and charts as graphics or csv.
9. Access app features by API with documentation and sample Jupyter Notebook.
10. Links to source code, installation instructions, GLDAS data downloads, documentation.

## API Documentation
This app provides a REST API to get timeseries data programmatically. You can query the API at the url ```[tethys_port_host]/apps/gldas/api/apiFunctionName```

**PLEASE REFER TO api-demo.ipynb IN THE APP DIRECTORY FOR A TUTORIAL** 

There are 5 API methods, 4 offer help/explanation and 1 for requesting data:
* ```help```
* ```timeOptions```
* ```variableOptions```
* ```geometryOptions```
* ```timeseries```

The API method timeseries requires 4 parameters as explained in the help/option API methods:
* ```variable```
* ```time```
* ```loc_type```
* ```coords``` or ```region```



### help (/apps/gldas/api/help)
* Parameters: none
* Returns: JSON object: contains explanations of each parameter and links to help
 
### timeOptions (/apps/gldas/api/timeOptions)
* Parameters: none
* Returns: JSON object: description of the available data and an explanation of how to format your request

### variableOptions (/apps/gldas/api/variableOptions)
* Parameters: none
* Returns: JSON object: contains a list of tuples with the full name of each variable and the shortened name that you need to use in API requests. 

### geometryOptions (/apps/gldas/api/geometryOptions)
* Parameters: none
* Returns: JSON object: instructions for formatting a list of coordinates for points/bounding boxes and a list of the available countries and world regions you may pick from.
  
### timeseries (/apps/gldas/api/timeseries)
* Parameters:  
    ```variable```  
    ```time```  
    ```loc_type```  
    ```coords``` or ```region```
* Returns: JSON object: contains the information to plot each of the 5 charts available in the app using the highcharts.js software package.

## Installation Instructions
### 1 Install the Tethys App
This application is compatible with Tethys 2.X and Tethys 3 Distributions and is compatible with both Python 2 and 3 and Django 1 and 2. Install the latest version of Tethys before installing this app. This app requires the python packages: numpy, netcdf4, ogr, osr. Both should be installed automatically as part of this installation process.

On the terminal of the server enter the tethys environment with the ```t``` command. ```cd``` to the directory where you install apps then run the following commands:  
~~~~
git clone https://github.com/rileyhales/gldas.git  
cd gldas
python setup.py develop
~~~~  
If you are on a production server, run:
~~~~
tethys manage collectstatic
~~~~
Reset the server, then attempt to log in through the web interface as an administrator. The app should appear in the Apps Library page in grey indicating you need to configure the custom settings.

### 2 Set up THREDDS and download GLDAS data
Refer to the documentation for Thredds to set up an instance of Thredds on your tethys server. In the thredds public folder, where your datasets are stored, create a new folder called ```gldas```. Get the path to this directory and save it for later. You need to fill this folder with the GLDAS data from NASA and there are 2 ways to do this.

1. Run the gldasworkflow.sh workflow found in the gldasworkflow folder of the app using the path to the ```gldas``` folder as the argument to the function.
2. Go to [disc.gsfc.nasa.gov](https://disc.gsfc.nasa.gov/datasets?keywords=gldas) and sign up for an Earth Data account. Download all the GLDAS 2 and 2.1 monthly, 1/4 degree resolution netcdf datasets. Create a directory inside the ```gldas``` folder called ```raw``` and save all the data here. Copy the contents of the ```gldasworkflow/ncml``` directory to the ```gldas``` directory

If you did it correctly, your folder should look like this:
~~~~
gldas
--->1950s.ncml
--->1960s.ncml
--->1970s.ncml
--->1980s.ncml
--->1990s.ncml
--->2000s.ncml
--->2010s.ncml
--->alltimes.ncml
    
--->raw (directory)
    ---><all the gldas datasets here>
~~~~
You will also need to modify Thredds' settings files to enable WMS services and support for netCDF files on your server. In the folder where you installed Thredds, there should be a file called ```catalog.xml```. 
~~~~
vim catalog.xml
~~~~
Type ```a``` to begin editing the document.

At the top of the document is a list of supported services. Make sure the line for wms is not commented out.
~~~~
<service name="wms" serviceType="WMS" base="/thredds/wms/" />
~~~~
Scroll down toward the end of the section that says ```filter```. This is the section that limits which kinds of datasets Thredds will process. We need it to accept .nc, .nc4, and .ncml file types. Make sure your ```filter``` tag includes the following lines.
~~~~
<filter>
    <include wildcard="*.nc4"/>
    <include wildcard="*.ncml"/>
</filter>
~~~~
Press ```esc``` then type ```:x!```  and press the ```return``` key to save and quit.
~~~~
vim threddsConfig.xml
~~~~
Find the section near the top about CORS (Cross-Origin Resource Sharing). CORS allows Thredds to serve data to servers besides the host where it is located. Depending on your exact setup, you need to enable CORS by uncommenting these tags.
~~~~
<CORS>
    <enabled>true</enabled>
    <maxAge>1728000</maxAge>
    <allowedMethods>GET</allowedMethods>
    <allowedHeaders>Authorization</allowedHeaders>
    <allowedOrigin>*</allowedOrigin>
</CORS>
~~~~
Press ```esc``` then type ```:x!```  and press the ```return``` key to save and quit.

Reset the Thredds server so the catalog is regenerated with the edits that you've made. The command to reset your server will vary based on your installation method, such as ```docker reset thredds``` or ```sudo systemctl reset tomcat```.

### 3 Set up a GeoServer (for user-uploaded shapefiles)
Refer to the documentation for GeoServer to set up an instance of GeoServer on your tethys server. If you choose not to use geoserver, your users will not be able to view custom shapefiles in the app.

This command asks you to specify:
* Geoserver Username and Password. If you have not changed it, the default is admin and geoserver.
* Name of the Zip Archive you're uploading. Be sure you spell it correctly and that you put it in each of the 2 places it is asked for.
* Hostname. The host website, e.g. ```tethys.byu.edu```.
* The Workspace URI. The URI that you specified when you created the new workspace through the web interface. If you followed these instructions it should be ```gldas```.

### 4 Set The Custom Settings
Log in to your Tethys portal as an admin. Click on the grey GLDAS box and specify these settings:
* **thredds_path:** This is the full path to the directory named gldas that you should have created within the thredds data directory during step 2. You can get this by navigating to that folder in the terminal and then using the ```pwd``` command. (example: ```/tomcat/content/thredds/gldas/```)  
* **thredds_url:** This is the base URL to Thredds WMS services that the app uses to build urls for each of the WMS layers generated for the netcdf datasets. If you followed the typical configuration of thredds (these instructions) then your base url will look something like ```yourserver.com/thredds/wms/testAll/gldas/```. You can verify this by opening the thredds catalog in a web browser (typically at ```yourserver.com/thredds/catalog.html```). Navigate to one of the GLDAS netcdf files and click the WMS link. A page showing an xml document should load. Copy the url in the address bar until you get to the ```/gldas/``` folder in that url. Do not include ```/raw/name_of_dataset.nc``` or the request that comes after. (example: ```https://tethys.byu.edu/thredds/wms/testAll/gldas/```)
* **Spatial Dataset Services:** Create a Tethys SpatialDatasetService configured with the correct urls and admin username/password for the GeoServer from step 3
