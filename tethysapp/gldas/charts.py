"""
Author: Riley Hales, 2018
Copyright: Riley Hales, RCH Engineering, 2019
Description: Functions for generating timeseries and simple statistical
    charts for netCDF data for point, bounding box, or shapefile geometries
"""
import calendar
import datetime as dt
import glob
import json
import os
import shutil

import geomatics as gm
import netCDF4 as nc

from .app import Gldas as App
from .options import gldas_variables


def newchart(data):
    """
    Determines the environment for generating a timeseries chart. Call this function
    """
    # response metadata items
    meta = {
        'variable': data['variable'],
        'loc_type': data['loc_type']
    }
    for item in gldas_variables():
        if item[1] == data['variable']:
            meta['name'] = item[0]
            break

    user_workspace = os.path.join(os.path.dirname(__file__), 'workspaces', 'user_workspaces', data['instance_id'])
    if os.path.exists(user_workspace):
        shutil.rmtree(user_workspace)
    os.mkdir(user_workspace)

    # list then filter the available netcdfs
    path = os.path.join(App.get_custom_setting('thredds_path'), 'raw')
    if len(data['time']) == 5:  # a decade choice
        files = glob.glob(os.path.join(path, f"*A{data['time'][0:3]}*.nc4"))
    elif len(data['time']) == 4:  # a year
        files = glob.glob(os.path.join(path, f"*A{data['time'][0:4]}*.nc4"))
    else:
        files = glob.glob(os.path.join(path, "*.nc4"))
    files.sort()

    meta['units'] = nc.Dataset(files[0], 'r')[data['variable']].__dict__['units']

    # get the timeseries, units, and message based on location type
    if data['loc_type'] == 'Point':
        timeseries = gm.timeseries.point(files, data['variable'], data['coords'], ('lon', 'lat'))
        meta['seriesmsg'] = 'At a Point'

    elif data['loc_type'] == 'Polygon':
        coords = data['coords'][0]
        coords = (
            (float(coords[0][0]), float(coords[0][1]),),
            (float(coords[2][0]), float(coords[2][1]),),
        )
        timeseries = gm.timeseries.bounding_box(files, data['variable'], coords[0], coords[1], ('lon', 'lat'))
        meta['seriesmsg'] = 'In a Bounding Box'

    elif data['loc_type'] == 'Shapefile':
        shp = [i for i in os.listdir(user_workspace) if i.endswith('.shp')]
        shp.remove('usergj.shp')
        shp = os.path.join(shp[0])
        timeseries = gm.timeseries.polygons(files, data['variable'], shp, ('lon', 'lat'))
        meta['seriesmsg'] = 'In User\'s Shapefile'

    elif data['loc_type'] == 'GeoJSON':
        shp = os.path.join(user_workspace, '__tempgj.shp')
        with open(os.path.join(user_workspace, 'usergj.geojson')) as f:
            gm.convert.geojson_to_shapefile(json.loads(f.read()), shp)
        timeseries = gm.timeseries.polygons(files, data['variable'], shp, ('lon', 'lat'))
        for file in glob.glob(os.path.join(user_workspace, '__tempgj.*')):
            os.remove(file)
        meta['seriesmsg'] = 'In User\'s GeoJSON'

    elif data['loc_type'].startswith('esri-'):
        esri_location = data['loc_type'].replace('esri-', '')
        geojson = gm.data.get_livingatlas_geojson(esri_location)
        shp = os.path.join(user_workspace, 'tmp.geojson')
        with open(shp, 'w') as tmp:
            tmp.write(json.dumps(geojson))
        timeseries = gm.timeseries.polygons(files, data['variable'], shp, ('lon', 'lat'))
        os.remove(shp)
        meta['seriesmsg'] = 'Within ' + esri_location

    times = []
    for file in files:
        try:
            times.append(dt.datetime.strptime(os.path.basename(file), 'GLDAS_NOAH025_M.A%Y%m.021.nc4'))
        except:
            times.append(dt.datetime.strptime(os.path.basename(file), 'GLDAS_NOAH025_M.A%Y%m.020.nc4'))
    timeseries['datetime'] = tuple(times)

    dates = timeseries['datetime'].dt.strftime('%Y-%m-%d')
    dates = dates.tolist()
    values = list(map(float, timeseries.values[:, 1].tolist()))

    if data['stats']:
        return {
            'meta': meta,
            'timeseries': list(zip(dates, values)),
            'stats': makestatplots(timeseries, data['time']),
        }
    else:
        return {
            'meta': meta,
            'timeseries': list(zip(dates, values)),
        }


def makestatplots(df, time):
    months = dict((n, m) for n, m in enumerate(calendar.month_name))
    yearmulti = []
    monthmulti = []
    yearbox = []
    monthbox = []

    if time == 'alltimes':
        ref_yr = 1948
        numyears = int(dt.datetime.now().strftime("%Y")) - ref_yr + 1  # +1 because we want the first year also
    else:
        ref_yr = int(time.replace('s', ''))
        numyears = 10
    years = [i + ref_yr for i in range(numyears)]

    df.index = df['datetime']
    del df['datetime']

    for i in range(1, 13):
        tmp = df[df.index.month == i].values
        ymin = min(tmp)
        ymax = max(tmp)
        mean = sum(tmp) / len(tmp)
        monthbox.append((months[i], list(map(float, tmp))))
        monthmulti.append((months[i], float(ymin), float(mean), float(ymax)))
    for year in years:
        tmp = df[df.index.year == year].values
        ymin = min(tmp)
        ymax = max(tmp)
        mean = sum(tmp) / len(tmp)
        yearbox.append((year, list(map(float, tmp))))
        yearmulti.append((year, float(ymin), float(mean), float(ymax)))

    return yearmulti, monthmulti, yearbox, monthbox
