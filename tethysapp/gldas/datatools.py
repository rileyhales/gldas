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
    tperiod = data['time']

    data_dir = '/home/rchales/thredds/gldas/'

    if tperiod == 'alltimes':
        path = os.path.join(data_dir, 'raw')
        files = os.listdir(path)
        print files
    else:
        path = os.path.join(data_dir, 'raw')
        allfiles = os.listdir(path)
        files = [nc for nc in allfiles if nc.startswith("GLDAS_NOAH025_M.A" + str(tperiod))]
        print files

    # find the point of data array that corresponds to the user's choice
    dataset = netCDF4.Dataset(path + '/' + str(files[0]), 'r')
    nc_lons = dataset['lon'][:]
    nc_lats = dataset['lat'][:]
    adj_lon_ind = (numpy.abs(nc_lons - coords[0])).argmin()
    adj_lat_ind = (numpy.abs(nc_lats - coords[1])).argmin()
    dataset.close()

    tstep = 0
    for nc in files:
        dataset = netCDF4.Dataset(path + '/' + nc, 'r')
        val = float(dataset[variable][0, adj_lat_ind, adj_lon_ind].data)
        values.append((tstep, val))
        tstep += 1
        dataset.close()

    # elif is_agg == False:
    #     tstep = 0
    #     for time, var in enumerate(dataset['time'][:]):
    #         val = float(dataset[variable][adj_lat_ind, adj_lon_ind, time].data)
    #         values.append((tstep, val))
    #         tstep += 1
    #     dataset.close()
    # timestep management
    # t_start = dataset['time'].__dict__['begin_date']
    # t_start = datetime.datetime.strptime(t_start, "%Y%m%d")
    # t_step = int(dataset['time'].__dict__['time_increment'])
    # for time, var in enumerate(dataset['time'][:]):
    #     val = float(dataset[variable][adj_lat_ind, adj_lon_ind, time].data)
    #     t_current = t_start + datetime.timedelta(days=t_step * time)
    #     timestamp = str(datetime.datetime.strftime(t_current, "%Y-%m-%d"))
    #     values.append((timestamp, val))

    return values
