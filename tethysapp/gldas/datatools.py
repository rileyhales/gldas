import netCDF4, numpy, datetime, os

# generates the plotable points based on the user inputs
def timeseries_plot(data):
    """
    Description: generates a timeseries for a given point and given variable defined by the user.
    Arguments: A dictionary object from the AJAX-ed JSON object that contains, the type of data, coordinates,
        and variable.
    Author: Riley Hales
    Dependencies: netcdf4, numpy, datetime, random
    Last Updated: Sept 19 2018
    """
    values = []
    variable = str(data['variable'])
    coords = data['coords']

    dataset_url = os.path.join('/home/rchales/thredds', str(variable) + '.nc')
    dataset = netCDF4.Dataset(dataset_url, 'r')

    # find the point of data array that corresponds to the user's choice
    nc_lons = dataset['lon'][:]
    nc_lats = dataset['lat'][:]

    # timestep management
    t_start = dataset['time'].__dict__['begin_date']
    t_start = datetime.datetime.strptime(t_start, "%Y%m%d")
    t_step = int(dataset['time'].__dict__['time_increment'])

    adj_lon_ind = (numpy.abs(nc_lons - coords[0])).argmin()
    adj_lat_ind = (numpy.abs(nc_lats - coords[1])).argmin()
    for time, var in enumerate(dataset['time'][:]):
        val = float(dataset[variable][adj_lat_ind, adj_lon_ind, time].data)
        t_current = t_start + datetime.timedelta(days=t_step * time)
        timestamp = str(datetime.datetime.strftime(t_current, "%Y-%m-%d"))
        values.append((timestamp, val))

    dataset.close()

    return values

    return [1,2,3,4,5,6,7,8,9,10]

# This function can be used to preprocess datasets
def merge_ncs_geo2D_ts(src_path, dst_path, var):
    """
    Description: Merges a directory of netcdfs each with data for 1 day into a properly formatted timeseries netcdf4.
        This function is meant for preprocessing purposes only and should not be called in the app.
    Arguments:
        src_path: string path to the DIRECTORY containing the source files, include the / at the end
        dst_path: string path to the DIRECTORY where the combined timeseries should be saved
        var: string name of the variable you want a timeseries for exactly as recorded in the source files
    Dependencies: netCDF4, os
    Author: Riley Hales
    Revised Date: Aug 31 2018
    """

    # list all the filed contained in the given source dir
    source_files = os.listdir(src_path)

    # create the new netcdf
    timeseries = netCDF4.Dataset(dst_path + var + '.nc', 'w', clobber=True, format='NETCDF4')

    # specify dimensions
    timeseries.createDimension('lon', 1480)
    timeseries.createDimension('lat', 960)
    timeseries.createDimension('time', len(source_files))

    # create the time variable the way it's supposed to be
    timeseries.createVariable(varname='time', datatype='i4', dimensions='time')
    timeseries['time'].setncattr('units', 'days since 2017-06-01 00:00:00')
    timeseries['time'].setncattr('time_increment', '1')
    timeseries['time'].setncattr('begin_date', '20170601')
    timeseries['time'].setncattr('begin_time', '000000')
    timeseries['time'].setncattr('name', 'time')
    daylist = []
    for i in range(len(source_files)):
        daylist.append(i)
    timeseries['time'][:] = daylist

    # create the latitude and longitude variables correctly 'lat' and 'lon'
    timeseries.createVariable(varname='lon', datatype='f4', dimensions='lon')
    timeseries.createVariable(varname='lat', datatype='f4', dimensions='lat')
    lat = 2.025
    lat_list = []
    while lat < 50:
        lat_list.append(lat)
        lat += .05
    lon = 49.025
    lon_list = []
    while lon < 123:
        lon_list.append(lon)
        lon += .05
    timeseries['lon'][:] = lon_list
    timeseries['lat'][:] = lat_list

    # create the variable the we want to make the time series for
    timeseries.createVariable(varname=var, datatype='f4', dimensions=('lat', 'lon', 'time'))

    # for every file in the folder, open file, assign variable variable data to current time step, next time step
    tstep = 0
    var_list = ['lat', 'lon']
    for file in source_files:
        # for each file in the folder, open the file
        source = netCDF4.Dataset(src_path + file)
        # set the global attributes, but only once
        if tstep < 1:
            timeseries.setncatts(source.__dict__)
        # copy the variable data to the appropriate places
        for name, variable in source.variables.items():
            # copy the variable specified by the user
            if name == var:
                timeseries[name][:, :, tstep] = source[name][:, :]
                tstep += 1
                # set the variable attributes, but only 1 time
                if tstep < 1:
                    for attr in source[name].__dict__:
                        if attr != "_FillValue":
                            timeseries[name].setncattr(attr, source[name].__dict__[attr])
            # copy the other variables, but only the first time because lat/lon is the same for all
            if name in var_list and tstep < 1:
                for attr in source[name].__dict__:
                    if attr != "_FillValue":
                        timeseries[name].setncattr(attr, source[name].__dict__[attr])
        source.close()

    # sync pushes the data to the disc, close removes the connections to the opened file
    timeseries.sync()
    timeseries.close()

    return()