import calendar
import datetime
import os
import shutil

import rasterio
import rasterstats
import netCDF4
import numpy
import pandas
import statistics

from .options import app_settings, gldas_variables
from .app import Gldas as App


def newchart(data):
    """
    Determines the environment for generating a timeseries chart
    :param data: a JSON object with params from the UI/API call
    :return:
    """
    # input parameters
    var = str(data['variable'])
    loc_type = data['loc_type']

    # list the netcdfs to be processed
    path = app_settings()['threddsdatadir']
    path = os.path.join(path, 'raw')
    allfiles = os.listdir(path)
    files = [nc for nc in allfiles if nc.endswith('.nc4')]
    if data['time'] != 'alltimes':
        files = [i for i in files if data['time'] in i]
    files.sort()

    # some metadata
    for item in gldas_variables():
        if item[1] == data['variable']:
            name = item[0]
            break

    # get the timeseries, units, and message based on location type
    if loc_type == 'Point':
        values, units = pointchart(var, data['coords'], path, files)
        type_message = 'Values at a Point'
    elif loc_type == 'Polygon':
        values, units = polychart(var, data['coords'], path, files)
        type_message = 'Averaged over a Polygon'
    elif loc_type == 'Shapefile':
        values, units = shpchart(var, path, files, data['region'], data['instance_id'])
        if data['region'] == 'customshape':
            type_message = 'Average for user\'s shapefile'
        else:
            type_message = 'Average for ' + data['region']
    values.sort(key=lambda tup: tup[0])

    resp = {'values': values, 'units': units, 'variable': var, 'type': type_message, 'name': name}
    if data['time'] == 'alltimes':
        resp['multiline'], resp['boxplot'], resp['categories'] = makestatplots(values)

    return resp


def pointchart(var, coords, path, files):
    """
    Description: generates a timeseries for a given point and given variable defined by the user.
    Arguments: A dictionary object from the AJAX-ed JSON object that contains coordinates and the variable name.
    Author: Riley Hales
    Dependencies: netcdf4, numpy, datetime, os, calendar, app_settings (options)
    Last Updated: Oct 11 2018
    """
    # return items
    values = []

    # get a list of the lat/lon and units using a reference file
    nc_obj = netCDF4.Dataset(os.path.join(path, files[0]), 'r')
    nc_lons = nc_obj['lon'][:]
    nc_lats = nc_obj['lat'][:]
    units = nc_obj[var].__dict__['units']
    # get the index number of the lat/lon for the point
    lon_indx = (numpy.abs(nc_lons - int(coords[0]))).argmin()
    lat_indx = (numpy.abs(nc_lats - int(coords[1]))).argmin()
    nc_obj.close()

    # extract values at each timestep
    for nc in files:
        # get the time value for each file
        nc_obj = netCDF4.Dataset(os.path.join(path, nc), 'r')
        time = nc_obj['time'].__dict__['begin_date']
        time = datetime.datetime.strptime(time, "%Y%m%d")
        # slice the array at the area you want
        val = float(nc_obj[var][0, lat_indx, lon_indx].data)
        values.append((calendar.timegm(time.utctimetuple()) * 1000, val, time.month, time.year))
        nc_obj.close()

    return values, units


def polychart(var, coords, path, files):
    """
    Description: generates a timeseries for a given point and given variable defined by the user.
    Arguments: A dictionary object from the AJAX-ed JSON object that contains coordinates and the variable name.
    Author: Riley Hales
    Dependencies: netcdf4, numpy, datetime, os, calendar, app_settings (options)
    Last Updated: May 14 2019
    """
    # return items
    values = []

    # get a list of the latitudes and longitudes and the units
    nc_obj = netCDF4.Dataset(os.path.join(path, str(files[0])), 'r')
    nc_lons = nc_obj['lon'][:]
    nc_lats = nc_obj['lat'][:]
    units = nc_obj[var].__dict__['units']
    # get a bounding box of the rectangle in terms of the index number of their lat/lons
    minlon = (numpy.abs(nc_lons - int(coords[0][1][0]))).argmin()
    maxlon = (numpy.abs(nc_lons - int(coords[0][3][0]))).argmin()
    maxlat = (numpy.abs(nc_lats - int(coords[0][1][1]))).argmin()
    minlat = (numpy.abs(nc_lats - int(coords[0][3][1]))).argmin()
    nc_obj.close()

    # extract values at each timestep
    for nc in files:
        # set the time value for each file
        nc_obj = netCDF4.Dataset(os.path.join(path, nc), 'r')
        time = nc_obj['time'].__dict__['begin_date']
        time = datetime.datetime.strptime(time, "%Y%m%d")
        # slice the array, drop nan values, get the mean, append to list of values
        array = nc_obj[var][0, minlat:maxlat, minlon:maxlon].data
        array[array < -5000] = numpy.nan  # If you have fill values, change the comparator to git rid of it
        array = array.flatten()
        array = array[~numpy.isnan(array)]
        values.append((calendar.timegm(time.utctimetuple()) * 1000, float(array.mean()), time.month, time.year))

        nc_obj.close()

    return values, units


def shpchart(var, path, files, region, instance_id):
    """
    Description: This script accepts a netcdf file in a geographic coordinate system, specifically the NASA GLDAS
        netcdfs, and extracts the data from one variable and the lat/lon steps to create a geotiff of that information.
    Dependencies: netCDF4, numpy, rasterio, rasterstats, os, shutil, calendar, datetime, app_settings (options)
    Params: View README.md
    Returns: Creates a geotiff named 'geotiff.tif' in the directory specified
    Author: Riley Hales, RCH Engineering, March 2019
    """
    # return items
    values = []

    # Remove old geotiffs before filling it
    wrkpath = App.get_app_workspace().path
    geotiffdir = os.path.join(wrkpath, 'geotiffs')
    if os.path.isdir(geotiffdir):
        shutil.rmtree(geotiffdir)
    os.mkdir(geotiffdir)

    # open the netcdf and get metadata
    nc_obj = netCDF4.Dataset(os.path.join(path, files[0]), 'r')
    lat = nc_obj.variables['lat'][:]
    lon = nc_obj.variables['lon'][:]
    units = nc_obj[var].__dict__['units']
    geotransform = rasterio.transform.from_origin(lon.min(), lat.max(), lat[1] - lat[0], lon[1] - lon[0])
    nc_obj.close()

    # read netcdf, create geotiff, zonal statistics, format outputs for highcharts plotting
    for nc in files:
        # open the netcdf and get the data array
        nc_obj = netCDF4.Dataset(os.path.join(path, nc), 'r')
        time = nc_obj['time'].__dict__['begin_date']
        time = datetime.datetime.strptime(time, "%Y%m%d")

        var_data = nc_obj.variables[var][:]  # this is the array of values for the nc_obj
        array = numpy.asarray(var_data)[0, :, :]  # converting the data type
        array[array < -9000] = numpy.nan  # use the comparator to drop nodata fills
        array = array[::-1]  # vertically flip array so tiff orientation is right (you just have to, try it)

        # file paths and settings
        if region == 'customshape':
            shppath = os.path.join(os.path.dirname(__file__), 'workspaces', 'user_workspaces', instance_id)
            shp = [i for i in os.listdir(shppath) if i.endswith('.shp')]
            shppath = os.path.join(shppath, shp[0])
        else:
            shppath = os.path.join(wrkpath, 'shapefiles', region, region.replace(' ', '') + '.shp')
        gtiffpath = os.path.join(wrkpath, 'geotiffs', 'geotiff.tif')

        with rasterio.open(gtiffpath, 'w', driver='GTiff', height=len(lat), width=len(lon), count=1, dtype='float32',
                           nodata=numpy.nan, crs='+proj=latlong', transform=geotransform) as newtiff:
            newtiff.write(array, 1)  # data, band number

        stats = rasterstats.zonal_stats(shppath, gtiffpath, stats="mean")
        values.append((calendar.timegm(time.utctimetuple()) * 1000, stats[0]['mean'], time.month, time.year))

    if os.path.isdir(geotiffdir):
        shutil.rmtree(geotiffdir)

    return values, units


def makestatplots(values):
    """
    Calculates statistics for the array of timeseries values and returns arrays for a highcharts boxplot
    Dependencies: statistics, pandas, datetime, calendar
    """
    df = pandas.DataFrame(values, columns=['timestamp', 'values', 'month', 'year'])
    multiline = {'yearmulti': {'min': [], 'max': [], 'mean': []},
                 'monthmulti': {'min': [], 'max': [], 'mean': []}}
    boxplot = {'yearbox': [], 'monthbox': []}

    months = dict((n, m) for n, m in enumerate(calendar.month_name))
    numyears = int(datetime.datetime.now().strftime("%Y")) - 1999  # not 2000 because we include that year
    categories = {'month': [months[i + 1] for i in range(12)], 'year': [i + 2000 for i in range(numyears)]}

    for i in range(1, 13):  # static 13 to go over months
        tmp = df[df['month'] == i]['values']
        std = statistics.stdev(tmp)
        median = statistics.median(tmp)
        ymin = min(tmp)
        ymax = max(tmp)
        mean = sum(tmp) / len(tmp)
        boxplot['monthbox'].append([months[i], ymin, mean - std, median, mean + std, ymax])
        multiline['monthmulti']['min'].append((months[i], ymin))
        multiline['monthmulti']['mean'].append((months[i], mean))
        multiline['monthmulti']['max'].append((months[i], ymax))
    for i in range(numyears):
        tmp = df[df['year'] == i + 2000]['values']
        std = statistics.stdev(tmp)
        median = statistics.median(tmp)
        ymin = min(tmp)
        ymax = max(tmp)
        mean = sum(tmp) / len(tmp)
        boxplot['yearbox'].append([i, ymin, mean - std, median, mean + std, ymax])
        multiline['yearmulti']['min'].append((i + 2000, ymin))
        multiline['yearmulti']['mean'].append((i + 2000, mean))
        multiline['yearmulti']['max'].append((i + 2000, ymax))

    return multiline, boxplot, categories
