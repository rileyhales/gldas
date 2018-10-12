import netCDF4, numpy, datetime, os

# generates the plotable points based on the user inputs
def ts_plot(data):
    """
    Description: generates a timeseries for a given point and given variable defined by the user.
    Arguments: A dictionary object from the AJAX-ed JSON object that contains coordinates and the variable name.
    Author: Riley Hales
    Dependencies: netcdf4, numpy, datetime, random
    Last Updated: Oct 11 2018
    """
    values = []
    variable = str(data['variable'])
    coords = data['coords']

    dataset_url = os.path.join('/home/rchales/thredds/gldas/preprocessed_ts', str(variable) + '.nc')
    dataset = netCDF4.Dataset(dataset_url, 'r')

    # find the point of data array that corresponds to the user's choice
    nc_lons = dataset['lon'][:]
    nc_lats = dataset['lat'][:]

    # timestep management
    # t_start = dataset['time'].__dict__['begin_date']
    # t_start = datetime.datetime.strptime(t_start, "%Y%m%d")
    # t_step = int(dataset['time'].__dict__['time_increment'])
    #
    # adj_lon_ind = (numpy.abs(nc_lons - coords[0])).argmin()
    # adj_lat_ind = (numpy.abs(nc_lats - coords[1])).argmin()
    # for time, var in enumerate(dataset['time'][:]):
    #     val = float(dataset[variable][adj_lat_ind, adj_lon_ind, time].data)
    #     t_current = t_start + datetime.timedelta(days=t_step * time)
    #     timestamp = str(datetime.datetime.strftime(t_current, "%Y-%m-%d"))
    #     values.append((timestamp, val))

    adj_lon_ind = (numpy.abs(nc_lons - coords[0])).argmin()
    adj_lat_ind = (numpy.abs(nc_lats - coords[1])).argmin()
    for time, var in enumerate(dataset['time'][:]):
        val = float(dataset[variable][adj_lat_ind, adj_lon_ind, time].data)
        values.append((time, val))

    dataset.close()

    return values

def ts_plot_agg(data):
    """
    Description: generates a timeseries for a given point and given variable from non-preprocessed nc files
    Arguments: A dictionary object from the AJAX-ed JSON object that contains coordinates and the variable name.
    Author: Riley Hales
    Dependencies: netcdf4, numpy, datetime, random
    Last Updated: Oct 11 2018
    """
    values = []
    variable = str(data['variable'])
    coords = data['coords']

    data_dir = '/home/rchales/thredds/gldas/raw_data/'
    files = os.listdir(data_dir)
    dataset = netCDF4.Dataset(data_dir + files[0], 'r')
    nc_lons = dataset['lon'][:]
    nc_lats = dataset['lat'][:]
    adj_lon_ind = (numpy.abs(nc_lons - coords[0])).argmin()
    adj_lat_ind = (numpy.abs(nc_lats - coords[1])).argmin()
    dataset.close()

    time = 1
    for nc in files:
        dataset = netCDF4.Dataset(data_dir + nc, 'r')
        val = float(dataset[variable][0, adj_lat_ind, adj_lon_ind].data)
        values.append((time, val))
        time += 1
        dataset.close()

    return values
