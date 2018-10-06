import netCDF4, numpy, datetime, os

# generates the plotable points based on the user inputs
def ts_plot(data):
    """
    Description: generates a timeseries for a given point and given variable defined by the user.
    Arguments: A dictionary object from the AJAX-ed JSON object that contains, the type of data, coordinates,
        and variable.
    Author: Riley Hales
    Dependencies: netcdf4, numpy, datetime, random
    Last Updated: Sept 26 2018
    """
    values = []
    variable = str(data['variable'])
    coords = data['coords']

    dataset_url = os.path.join('/home/rchales/thredds/gldas', str(variable) + '.nc')
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
