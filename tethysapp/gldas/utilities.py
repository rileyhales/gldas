import string
import random
import os
import datetime

from .app import Gldas as App


def new_id():
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for i in range(10))


def get_times():
    path = App.get_custom_setting('thredds_path')
    path = os.path.join(path, 'raw')
    files = os.listdir(path)
    files.sort()
    try:
        start = datetime.datetime.strptime(files[0], "GLDAS_NOAH025_M.A%Y%m.020.nc4").strftime("%B %Y")
    except ValueError:
        start = datetime.datetime.strptime(files[0], "GLDAS_NOAH025_M.A%Y%m.021.nc4").strftime("%B %Y")
    try:
        end = datetime.datetime.strptime(files[-1], "GLDAS_NOAH025_M.A%Y%m.020.nc4").strftime("%B %Y")
    except ValueError:
        end = datetime.datetime.strptime(files[-1], "GLDAS_NOAH025_M.A%Y%m.021.nc4").strftime("%B %Y")
    return {
        'oldest': start,
        'newest': end,
    }
