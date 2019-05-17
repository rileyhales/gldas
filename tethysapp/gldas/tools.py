import calendar
import datetime
import os
import shutil

import gdal
import gdalnumeric
import netCDF4
import numpy
import osr
import ogr
import json
import statistics
import pandas

from .app import Gldas as App
from .model import app_configuration


def pointchart(data):
    """
    Description: generates a timeseries for a given point and given variable defined by the user.
    Arguments: A dictionary object from the AJAX-ed JSON object that contains coordinates and the variable name.
    Author: Riley Hales
    Dependencies: netcdf4, numpy, datetime, os, calendar, app_configuration (model)
    Last Updated: Oct 11 2018
    """
    values = []
    variable = str(data['variable'])
    coords = data['coords']
    tperiod = data['time']

    configs = app_configuration()
    data_dir = configs['threddsdatadir']

    path = os.path.join(data_dir, 'raw')
    allfiles = os.listdir(path)
    if tperiod == 'alltimes':
        files = [nc for nc in allfiles if nc.startswith("GLDAS_NOAH025_M.A")]
        files.sort()
    else:
        files = [nc for nc in allfiles if nc.startswith("GLDAS_NOAH025_M.A" + str(tperiod))]
        files.sort()

    # find the point of data array that corresponds to the user's choice, get the units of that variable
    dataset = netCDF4.Dataset(os.path.join(path, str(files[0])), 'r')
    nc_lons = dataset['lon'][:]
    nc_lats = dataset['lat'][:]
    adj_lon_ind = (numpy.abs(nc_lons - coords[0])).argmin()
    adj_lat_ind = (numpy.abs(nc_lats - coords[1])).argmin()
    units = dataset[variable].__dict__['units']
    dataset.close()

    # extract values at each timestep
    for nc in files:
        # set the time value for each file
        dataset = netCDF4.Dataset(path + '/' + nc, 'r')
        t_value = (dataset['time'].__dict__['begin_date'])
        t_step = datetime.datetime.strptime(t_value, "%Y%m%d")
        month = t_step.month
        year = t_step.year
        t_step = calendar.timegm(t_step.utctimetuple()) * 1000
        for time, var in enumerate(dataset['time'][:]):
            # get the value at the point
            val = float(dataset[variable][0, adj_lat_ind, adj_lon_ind].data)
            values.append((t_step, val, month, year))
        dataset.close()

    return units, values


def polychart(data):
    """
    Description: generates a timeseries for a given point and given variable defined by the user.
    Arguments: A dictionary object from the AJAX-ed JSON object that contains coordinates and the variable name.
    Author: Riley Hales
    Dependencies: netcdf4, numpy, datetime, os, calendar, app_configuration (model)
    Last Updated: May 14 2019
    """
    values = []
    variable = str(data['variable'])
    coords = data['coords'][0]          # 5x2 array 1 row of lat/lon per corner, 1st duplicated (start/stop)
    tperiod = data['time']

    configs = app_configuration()
    data_dir = configs['threddsdatadir']

    path = os.path.join(data_dir, 'raw')
    allfiles = os.listdir(path)
    if tperiod == 'alltimes':
        files = [nc for nc in allfiles if nc.startswith("GLDAS_NOAH025_M.A")]
    else:
        files = [nc for nc in allfiles if nc.startswith("GLDAS_NOAH025_M.A" + str(tperiod))]
    files.sort()

    # find the point of data array that corresponds to the user's choice, get the units of that variable
    dataset = netCDF4.Dataset(os.path.join(path, str(files[0])), 'r')
    nc_lons = dataset['lon'][:]
    nc_lats = dataset['lat'][:]
    # get a lat/lon bounding box for the drawing
    minlon = (numpy.abs(nc_lons - coords[1][0])).argmin()
    maxlon = (numpy.abs(nc_lons - coords[3][0])).argmin()
    maxlat = (numpy.abs(nc_lats - coords[1][1])).argmin()
    minlat = (numpy.abs(nc_lats - coords[3][1])).argmin()
    units = dataset[variable].__dict__['units']
    dataset.close()

    # extract values at each timestep
    for nc in files:
        # set the time value for each file
        dataset = netCDF4.Dataset(path + '/' + nc, 'r')
        t_value = (dataset['time'].__dict__['begin_date'])
        t_step = datetime.datetime.strptime(t_value, "%Y%m%d")
        month = t_step.month
        year = t_step.year
        t_step = calendar.timegm(t_step.utctimetuple()) * 1000
        for time, var in enumerate(dataset['time'][:]):
            # get the value at the point
            array = dataset[variable][0, minlat:maxlat, minlon:maxlon].data
            array[array < -9000] = numpy.nan  # If you have fill values, change the comparator to git rid of it
            array = array.flatten()
            array = array[~numpy.isnan(array)]
            values.append((t_step, float(array.mean()), month, year))
        dataset.close()

    return units, values


def nc_to_gtiff(data):
    """
    Description: This script accepts a netcdf file in a geographic coordinate system, specifically the NASA GLDAS
        netcdfs, and extracts the data from one variable and the lat/lon steps to create a geotiff of that information.
    Dependencies: netCDF4, numpy, gdal, osr, os, shutil, calendar, datetime, App (app), app_configuration (model)
    Params: View README.md
    Returns: Creates a geotiff named 'geotiff.tif' in the directory specified
    Author: Riley Hales, RCH Engineering, March 2019
    """
    var = str(data['variable'])
    tperiod = data['time']
    configs = app_configuration()
    data_dir = configs['threddsdatadir']
    times = []
    units = ''

    path = os.path.join(data_dir, 'raw')
    allfiles = os.listdir(path)
    if tperiod == 'alltimes':
        files = [nc for nc in allfiles if nc.startswith("GLDAS_NOAH025_M.A")]
    else:
        files = [nc for nc in allfiles if nc.startswith("GLDAS_NOAH025_M.A" + str(tperiod))]
    files.sort()

    # Remove old geotiffs before filling it
    geotiffdir = os.path.join(App.get_app_workspace().path, 'geotiffs')
    if os.path.isdir(geotiffdir):
        shutil.rmtree(geotiffdir)
    os.mkdir(geotiffdir)

    for i in range(len(files)):
        # open the netcdf and copy data from it
        nc_obj = netCDF4.Dataset(os.path.join(path, str(files[i])), 'r')
        var_data = nc_obj.variables[var][:]
        lat = nc_obj.variables['lat'][:]
        lon = nc_obj.variables['lon'][:]
        units = nc_obj[var].__dict__['units']

        # create the timesteps for the highcharts plot
        t_value = (nc_obj['time'].__dict__['begin_date'])
        t_step = datetime.datetime.strptime(t_value, "%Y%m%d")
        times.append(calendar.timegm(t_step.utctimetuple()) * 1000)

        # format the array of information going to the tiff
        array = numpy.asarray(var_data)[0, :, :]
        array[array < -9000] = numpy.nan                # change the comparator to git rid of the fill value
        array = array[::-1]       # vertically flip the array so the orientation is right (you just have to, try it)

        # Creates geotiff raster file (filepath, x-dimensions, y-dimensions, number of bands, datatype)
        gtiffpath = os.path.join(geotiffdir, 'geotiff' + str(i) + '.tif')
        gtiffdriver = gdal.GetDriverByName('GTiff')
        new_gtiff = gtiffdriver.Create(gtiffpath, len(lon), len(lat), 1, gdal.GDT_Float32)

        # geotransform (sets coordinates) = (x-origin(left), x-width, x-rotation, y-origin(top), y-rotation, y-width)
        yorigin = lat.max()
        xorigin = lon.min()
        xres = lat[1] - lat[0]
        yres = lon[1] - lon[0]
        new_gtiff.SetGeoTransform((xorigin, xres, 0, yorigin, 0, -yres))

        # Set projection of the geotiff (Projection EPSG:4326, Geographic Coordinate System WGS 1984 (degrees lat/lon)
        new_gtiff.SetProjection(osr.SRS_WKT_WGS84)

        # actually write the data array to the tiff file and save it
        new_gtiff.GetRasterBand(1).WriteArray(array)      # write band to the raster (variable array)
        new_gtiff.FlushCache()                            # write to disk
    return times, units


def rastermask_average_gdalwarp(data):
    """
    Description: A function to mask/clip a raster by the boundaries of a shapefile and computer the average value of the
        resulting raster
    Dependencies:
        gdal, gdalnumeric, numpy, os, shutil, ogr, json
        from .app import Gldas as App
    Params: View README.md
    Returns: mean value of an array within a shapefile's boundaries
    Author: Riley Hales, RCH Engineering, April 2019
    """

    values = []
    times = data['times']
    times.sort()
    shppath = ''
    wrkpath = App.get_app_workspace().path

    if data['shapefile'] == 'true':
        region = data['region']
        shppath = os.path.join(wrkpath, 'shapefiles', region, region.replace(' ', '') + '.shp')
    else:
        # todo: still under development- turn a geojson into a shapefile
        import shapefile
        from pyproj import Proj, transform
        # convert the geojson to a shapefile object
        coords = data['coords'][0]
        shape = shapefile.Writer(shppath, shapeType=shapefile.POLYGON, shp=coords)
        shape.close()

        driver = ogr.GetDriverByName('ESRI Shapefile')
        srs = osr.SpatialReference().ImportFromEPSG(4326)
        print(srs)
        datasource = driver.CreateDataSource(shppath)
        polygon = ogr.CreateGeometryFromJson(json.dumps(data['geojson']))
        fieldDefn_ = ogr.FieldDefn('id', ogr.OFTInteger)
        layer = datasource.CreateLayer('polygon', srs, ogr.wkbPolygon)
        layer.CreateField(fieldDefn_)
        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetGeometry(polygon)
        feature.SetField('id', 1)
        layer.CreateFeature(feature)

    # setup the working directories for the geoprocessing
    geotiffdir = os.path.join(wrkpath, 'geotiffs')
    geotiffs = os.listdir(geotiffdir)

    # perform the gropreccesing on each file in the geotiff directory
    for i in range(len(geotiffs)):
        # clip the raster
        inraster = gdal.Open(os.path.join(geotiffdir, 'geotiff' + str(i) + '.tif'))
        savepath = os.path.join(geotiffdir, 'outraster.tif')
        clippedraster = gdal.Warp(savepath, inraster, format='GTiff', cutlineDSName=shppath, dstNodata=numpy.nan)
        # do the averaging math on the raster as an array
        array = gdalnumeric.DatasetReadAsArray(clippedraster)
        array = array.flatten()
        array = array[~numpy.isnan(array)]
        mean = array.mean()
        values.append((times[i], float(mean)))

    if os.path.isdir(geotiffdir):
        shutil.rmtree(geotiffdir)

    return values

def determinestats(data):
    """
    Calculates statistics for the array of timeseries values and returns arrays for a highcharts boxplot
    Dependencies: statistics, pandas, datetime
    """
    df = pandas.DataFrame(data['values'], columns=['dates', 'values', 'month', 'year'])
    data['statistics'] = []

    if data['time'] == 'alltimes':
        for i in range(1, 13):
            tmp = df[df['month'] == i]['values']
            std = statistics.stdev(tmp)
            mean = sum(tmp)/len(tmp)
            data['statistics'].append([i, min(tmp), mean - std, mean, mean + std, max(tmp)])

    return data
