def ts_plot(data):
    """
    Description: generates a timeseries for a given point and given variable defined by the user.
    Arguments: A dictionary object from the AJAX-ed JSON object that contains coordinates and the variable name.
    Author: Riley Hales
    Dependencies: netcdf4, numpy, datetime, random
    Last Updated: Oct 11 2018
    """
    from .model import app_configuration
    import netCDF4, numpy, datetime, os, calendar

    values = []
    variable = str(data['variable'])
    coords = data['coords']
    tperiod = data['time']

    configs = app_configuration()
    data_dir = configs['threddsdatadir']

    path = os.path.join(data_dir, 'raw')
    if tperiod == 'alltimes':
        files = os.listdir(path)
        files.sort()
    else:
        allfiles = os.listdir(path)
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
        t_step = calendar.timegm(t_step.utctimetuple()) * 1000
        for time, var in enumerate(dataset['time'][:]):
            # get the value at the point
            val = float(dataset[variable][0, adj_lat_ind, adj_lon_ind].data)
            values.append((t_step, val))
        dataset.close()

    return_items = [units, values]

    return return_items


def nc_to_gtiff(data):
    """
    Description: This script accepts a netcdf file in a geographic coordinate system, specifically the NASA GLDAS
        netcdfs, and extracts the data from one variable and the lat/lon steps to create a geotiff of that information.
    Dependencies: netCDF4, numpy, gdal, osr
    Params: View README.md
    Returns: Creates a geotiff named 'geotiff.tif' in the directory specified
    Author: Riley Hales, RCH Engineering, March 2019
    """
    import netCDF4, numpy, gdal, osr, os, shutil
    from .model import app_configuration
    from .app import Gldas as App

    var = str(data['variable'])
    tperiod = data['time']
    configs = app_configuration()
    data_dir = configs['threddsdatadir']

    path = os.path.join(data_dir, 'raw')
    allfiles = os.listdir(path)
    if tperiod == 'alltimes':
        files = [nc for nc in allfiles if nc.startswith("GLDAS_NOAH025_M.A" + str(2019))]
        files.sort()
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

    return


