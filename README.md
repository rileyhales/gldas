# GLDAS Data Visualizer Documentation
This is a Tethys 2/3 compatible app that visualizes data from the NASA GES Disc website. It was developed to show ¼ degree resolution netcdf4 (.nc4) datasets with monthly averages. Datasets of other resolutions and for other time-periods may also work.

© Riley Hales, 2019. Developed at the BYU Hydroinformatics Lab.

## App Features
1. View time-animated maps of all GLDAS variables. Customize color scheme, opacity, animation/playback speed, time period.
2. View world region boundaries. Customize color scheme and opacity. Choose to get layers from Geoserver or local GeoJSON
3. View the Latitude/Longitude Coordinates of anywhere on the planet by hovering your mouse over the map.
4. Toggle visibility of controls and the controls menu.
5. Use drawing controls to place a point or draw a rectangle on the globe and generate a chart with timeseries values at that point or of the spatial average within the box.
6. Click on a landmass and a pop-up bubble gives you the name of the region and the option to generate a timeseries of average values in that region.
7. Choose between 4 additional chart options using box plots and multi-line plots to view statistical analysis of historical data.
8. Export timeseries charts as graphics.
9. Export timeseries data to csv.
10. Link to demonstration video on YouTube.
11. In-App tutorial explaining app features.
12. Links to source code, installation instructions, and GLDAS data downloads.
13. NCML files scan folders so they dont need to be updated each time data are added.

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

### 2 Set up a Thredds Server (GLDAS Rasters)
Refer to the documentation for Thredds to set up an instance of Thredds on your tethys server.

In the public folder where your datasets are stored, create a new folder called ```gldas```. Within that folder, place all the contents of the ncml folder in the app you downloaded in the previous step. Create a new folder called ```raw``` and leave it empty. You will fill it with data in the next step. 

In the app's folder you downloaded from git, copy the contents of the ```ncml``` folder into the ```gldas``` directory you just created in Thredds. These files are a form of xml called NetCDF Markup Language (.ncml). They filter the datasets in the raw folder by year and create an virtual aggregation of their data. You should not need to change these files when you get new datasets each month, but you will need to add a new one each year.

If you did it correctly, your folder should look like this:
~~~~
gldas
--->2000.ncml
--->2001.ncml
--->2002.ncml
    ...
--->2019.ncml
--->alltimes.ncml
    
--->raw
    ---><empty directory>
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
    <include wildcard="*.nc"/>
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

### 3 Get the GLDAS Data from NASA GES Disc
The datasets shown in this app are available at: https://disc.gsfc.nasa.gov/datasets?keywords=gldas&page=1. Follow the necessary steps on their website to get credentials and use the batch download commands. Do not change the file names.

You will save this data to the ```raw``` folder you created in the previous step. Verify that you have 12 netcdf files per year plus any files for the current year. Your thredds folder should now look like this:
~~~~
gldas
    ...
--->alltimes.ncml
    
--->raw
    --->GLDAS_NOAH025_M.A200001.021.nc4
    --->GLDAS_NOAH025_M.A200002.021.nc4
        ...    
~~~~

Verify that you have completed steps 2 and 3 correctly by viewing the Thredds catalog through a web browser. The default address will be something like ```yourserver.com/thredds/catalog.html```. Navigate to the ```Test all files...``` folder. Your ```gldas``` folder should be visible. Open it and check that all your ```.ncml``` files are visible and that the ```.nc4``` files are visible in the ```/raw``` directory. If they are not, review steps 2 and 3 and restart your Thredds server.

### 4 Set up a GeoServer (World Region Boundaries) (Optional, Recommended)
Refer to the documentation for GeoServer to set up an instance of GeoServer on your tethys server. If you choose not to use geoserver, skip this step and follow instructions in step 5 for the custom settings.

This app can display and perform spatial averaging for 8 world regions. The app will perform the raster operations and averaging using shapefiles that cover general regions of the globe in as few points as possible to increase computation speed, reduce file sizes, and prevent computation errors related to large and complex polygon shapefiles. More accurate boundaries for the regions are available for visualization as a Web Feature Service (WFS) through GeoServer or as local geojson files. A copy of the shapefiles you need, in the properly formatted zip archives, is found in the ```workspaces/app_workspace``` directory of the app.   

Use a web browser to log in to your GeoServer. Use the web interface to create a new workspace named ```gldas```. Use the command line to navigate to the directory containing the GeoServerFiles zip archive you got from the app. Extract the contents of that zip archive, but do not unzip the 8 zip archives that it contains. Upload each of those 8 zip archives to the new GeoServer workspace using cURL commands (e.g. run this command 8 times). The general format of the command is:
~~~~
curl -v -u [user]:[password] -XPUT -H "Content-type: application/zip" --data-binary @[name_of_zip].zip https://[hostname]/geoserver/rest/workspaces/[workspaceURI]/datastores/[name_of_zip]/file.shp
~~~~
This command asks you to specify:
* Geoserver Username and Password. If you have not changed it, the default is admin and geoserver.
* Name of the Zip Archive you're uploading. Be sure you spell it correctly and that you put it in each of the 2 places it is asked for.
* Hostname. The host website, e.g. ```tethys.byu.edu```.
* The Workspace URI. The URI that you specified when you created the new workspace through the web interface. If you followed these instructions it should be ```gldas```.

### 5 Set The Custom Settings
Log in to your Tethys portal as an admin. Click on the grey GLDAS box and specify these settings:

**Local File Path:** This is the full path to the directory named gldas that you should have created within the thredds data directory during step 2. You can get this by navigating to that folder in the terminal and then using the ```pwd``` command. (example: ```/tomcat/content/thredds/gldas/```)  

**Thredds Base Address:** This is the base URL to Thredds WMS services that the app uses to build urls for each of the WMS layers generated for the netcdf datasets. If you followed the typical configuration of thredds (these instructions) then your base url will look something like ```yourserver.com/thredds/wms/testAll/gldas/```. You can verify this by opening the thredds catalog in a web browser (typically at ```yourserver.com/thredds/catalog.html```). Navigate to one of the GLDAS netcdf files and click the WMS link. A page showing an xml document should load. Copy the url in the address bar until you get to the ```/gldas/``` folder in that url. Do not include ```/raw/name_of_dataset.nc``` or the request that comes after. (example: ```https://tethys.byu.edu/thredds/wms/testAll/gldas/```)

**Geoserver Workspace Address:** This is the WFS (ows) url to the workspace on geoserver where the shapefiles for the world region boundaries are served. This geoserver workspace needs to have at minimum WFS services enabled. You can find it by using the layer preview interface of GeoServer and choosing GeoJSON as the format. If you chose not to use geoserver, enter ```geojson``` as your url. (example: ```https://tethys.byu.edu/geoserver/gldas/ows```)

## How the app works
The various functions of the app are split into either python or javascript files named for what they control.
#### Javascript Files
* **bounds.js**: Contains a json object that has the minimum/maximum values of each variable arranged by year. These are used to get the color schemes of the map appropriately scaled.
* **highcharts.js**: Functions for controlling the tables that appear in the app.
* **leaflet.js**: A collection of functions for interacting with the leaflet javascript mapping api.
* **main.js**: Calls the mapping functions in exactly the correct order to make the maps and animations work. Also has listeners to change the map when the user changes the controls

#### Python Files
* **app.py**: Django app declarations, URL maps that connect the user's URL to the correct python function to control that page, Custom setting declarations.
* **ajax.py**: Contains 1 function for each URL map and ajax call made in javascript - all of the same name.
* **model.py**: Dictionaries of information that specify the available time periods, color schemes, variables, and so forth.
* **controllers.py**: The controller for the primary page of the app.
* **tools.py**: Tools used by the app to process data including making the timeseries of data.
* **api.py**: Limited functions for accessing data available through the app interface.
