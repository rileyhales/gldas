# GLDAS Data Visualizer Documentation
This is a Tethys 2/3 compatible app that visualizes data from the nasa gesdisc website. It was developed using the ¼ degree resolution netcdf4 (.nc4) datasets with monthly averages but other datasets with monthly averages should also work.

Developed by Riley Hales in 2018 at the BYU Hydroinformatics Lab.

## Install the App
On the terminal of the server enter the tethys environment then run:  
~~~~
git clone https://github.com/rileyhales/gldas.git  
cd gldas
python setup.py develop
~~~~  
If you are on a production server, run this command and reset the server
~~~~
tethys manage collectstatic
~~~~

This app uses two python packages that should be installed for you when you run the develop command.
* netCDF4, any version
* numpy, any version

## Get the GLDAS Data from NASA GES Disc
The datasets shown in this app are available at: https://disc.gsfc.nasa.gov/datasets?keywords=gldas&page=1. When using this app, do not change the file names. You should use the naming conventions used by NASA for the file names. Follow the necessary steps on their website to get credentials and use the batch download commands.

You will save this data to a folder within the directory containing all the data served by the thredds server you're using. Within that directory make another directory called gldas. In that folder put all the .ncml files found in the app's ncml directory and then create another folder called 'raw'. All the netcdf datasets you got from NASA GES Disc should be saved within this raw folder.  

Data is aggregated by year using NetCDF Markup Language (.ncml). The files you need are in the ncml folder of this app. If you need to modify the years you want to show, modify the existing files and use the naming convention shown (4 digit year and .ncml eg 2004.ncml.) Keep the changed files in the folder where you keep the datasets for Thredds. In the same folder, include another folder named raw. Inside the raw folder, place all the .nc4 datasets you got from NASA without changing names, preprocessing data, etc.

### Set The Custom Settings
You need to specify 2 custom settings when you install the app. The file path to where you are storing the gldas netCDF files locally on the server and the base wms URL for the thredds server that will be serving the data.

**Local File Path:** This is the path to the directory named gldas that you should have already created within the thredds data directory. You can get this by navigating to that folder in the terminal and then using the ```pwd``` command. (example: /home/tethys/Thredds/gldas/)  

**WMS base address:** This is the address that the app will use to get the OGC WMS layers for the netcdf datasets. You can find this by using your web browser to navigate the thredds server, typically located at ```yourserveraddress.com/thredds```. Find one of the datasets you want to show and click on the wms service link. When you see the XML, copy the address up until the name of the dataset that you clicked on and including the http. (example: https://tethys.byu.edu/thredds/wms/testAll/gldas/)
