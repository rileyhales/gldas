# GLDAS Data Visualizer Documentation
This is a Tethys 2/3 compatible app that visualizes data from the NASA GES Disc website. It was developed to show ¼ degree resolution netcdf4 (.nc4) datasets with monthly averages. Datasets of other resolutions and for other time-periods may also work.

The app shows time-animated maps and generates charts with a timeseries of values for a GLDAS variable either at a point or the spatial average within a polygon.

Developed by Riley Hales in 2018 at the BYU Hydroinformatics Lab.

## 1 Install the Tethys App
This application is compatible with Tethys 2.X and Tethys 3 Distributions and is compatible with both Python 2 and 3 and Django 1 and 2. Install the latest version of Tethys before installing this app. This app requires 2 python packages: numpy and netcdf4. Both should be installed automatically as part of this installation process.

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
Reset the server then attempt to log in through the web interface as an administrator. The app should appear in the Apps Library page in grey indicating you need to configure the custom settings.

## 2 Set up your Thredds Server
Refer to the documentation for Thredds to set up an instance of Thredds on your server.

In the public folder where your datasets are stored, create a new folder called ```gldas```. Within that folder, place all the contents of the ncml folder in the app you downloaded in the previous step. Create a new folder called ```raw``` and leave it empty. You will fill it with data in the next step. 

Data is aggregated by year using NetCDF Markup Language (.ncml). The files you need are in the ncml folder of the app and you should copy them to the Thredds folder you just created. When you add new datasets each month, you will need to modify the ncml file for the appropriate year to include the new dataset in your aggregation. If you need to modify the years you want to show, modify the existing files and use the naming convention shown (4 digit year and .ncml eg 2004.ncml.) These files look for the file called raw then filter the datasets within by name to create the aggregation. It is important that you use the exact file structure and naming conventions for these datasets used by NASA. Though you need to modify a file each time you add a new dataset, this prevents you from postprocessing years of GLDAS data each month.

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
Find the section near the top about CORS (Cross-Origin Resource Sharing). CORS allows Thredds to serve data to servers besides the host where it is located. Depending on your exact setup, you need to enable CORS by uncommenting the tags.
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

You'll need to reset the Thredds server so the catalog is regenerated with the edits that you've made. The command to reset your server will vary based on your installation method such as ```docker reset thredds``` or ```sudo systemctl reset tomcat```.

## 3 Get the GLDAS Data from NASA GES Disc
The datasets shown in this app are available at: https://disc.gsfc.nasa.gov/datasets?keywords=gldas&page=1. When using this app, do not change the file names. You should use the naming conventions used by NASA for the file names. Follow the necessary steps on their website to get credentials and use the batch download commands.

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

## 4 Set The Custom Settings
You need to specify 2 custom settings when you install the app. The file path to where you are storing the gldas netCDF files locally on the server and the base wms URL for the thredds server that will be serving the data.

**Local File Path:** This is the full path to the directory named gldas that you should have created within the thredds data directory during step 2. You can get this by navigating to that folder in the terminal and then using the ```pwd``` command. (example: ```/tomcat/content/thredds/gldas/```)  

**WMS base address:** This is the base that the app uses to build urls for each of the OGC WMS layers for the netcdf datasets. If you followed the typical configuration of thredds (these instructions) then your base url will look something like ```yourserver.com/thredds/wms/testAll/gldas/```. You can verify this by opening the thredds catalog in a web browser (typically at ```yourserver.com/thredds/catalog.html```). Navigate to one of the GLDAS netcdf files and click the WMS link. A page showing an xml document should load. Copy the url in the address bar until you get to the ```/gldas/``` folder in that url. Do not include ```/raw/name_of_dataset.nc``` or the request info that comes after it. (example: ```https://tethys.byu.edu/thredds/wms/testAll/gldas/```)

## How the app works
The various functions of the app are split into either python or javascript files named for what they control.
#### Javascript Files
* **data.js**: Contains a json object that has the minimum/maximum values of each variable arranged by year. These are used to get the color schemes of the map appropriately scaled.
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
