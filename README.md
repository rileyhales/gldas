# GLDAS Data Visualizer Documentation
# Data and Data Structure
This app accepts data from the nasa gesdisc website. Use ¼ degree resolution netcdf4 (.nc4) datasets with monthly averages. When using this app, do not change the file names. You should use the naming conventions used by NASA for the file names.

Data is aggegated by year using NetCDF Markup Language (.ncml). The files you need are in the ncml folder of this app. If you need to modify the years you want to show, modify the existing files and use the naming convention shown (4 digit year and .ncml eg 2004.ncml.) Keep the changed files in the folder where you keep the datasets for Thredds. In the same folder, include another folder named raw. Inside the raw folder, place all the .nc4 datasets you got from NASA without changing names, preprocessing data, etc.

The datasets are available at: https://disc.gsfc.nasa.gov/datasets?keywords=gldas&page=1

### Python Package Dependencies
* netCDF4
* oauth2client (required for google analytics)
* apiclient (google analytics api interface)
* os
* numpy
* datetime
* calendar
* ast
* math

### Custom Settings
You need to specify 2 custome settings when you install the app. The file path to where you are storing the gldas netCDF files locally on the server and the base wms URL for the thredds server that will be serving the data.   
On tethys.byu.edu the correct custom settings are:  
**Local File Path:** /home/tethys/Thredds/gldas/  
**WMS base address:** https://tethys.byu.edu/thredds/wms/testAll/gldas/

## Understanding the Code
### HTML
The app consists of a single page coded in home.html and base.html. Base.html contains all the links to import javascript or css styling code for leaflet and highcharts and also all the code for the 2 modals at the top of the page. Home.html has a variety of empty divs and Django tags that all get filled when the page is loaded. The content displayed on that page is a combination of tethys gizmos for manipulating input options and JavaScript to load a Leaflet map and Highcharts chart.

### Javascript
The JS is run out of the main.js file. In that file, cookies and global variables are set and then a JQuery section after document ready. That portion of the code calls leaflet.js and highcharts.js functions to populate the page. It also calls ajaxfunctions.js and data.js to get both constant data and dynamically calculated data. Each of the functions from ajaxFunctions.js has a companion function in the python ajaxhandlers.py file.

### Python
**App.py**  
Class Declaration  
**Api.py:**  
Returns JSON data for some of the information provided by the app
**Resources.py:**  
app parameters are processed here including: available variables, year intervals, Map locations to zoom to, results of the custom settings and app workspace paths, available metrics from google analytics, color scales, and available variables.  
**Controllers.py:**  
handles the content that gets put in the django tags on the home.html page  
**Ajaxhandlers.py:**  
contains 1 function to handle the data requested by leaflet or highcharts in each ajaxfunctions.js function. 1:1 ratio.  
**Datatools.py:**  
conatins functions for extracting data from the netcdf files, specifically creating the timeseries points to be plotted by highcharts.
Using the App
The app is used by zooming to certain regions, using the tool in the map interface to click a point, viewing the timeseries of values for the given variable, time, and location pairing.

The chart will regenerate itself when the time or variable is changed.
The timeseries animation on the map will continue when you change colors, variables or times.
When you load all available data, the chart and map will take noticeably longer to initially load.
