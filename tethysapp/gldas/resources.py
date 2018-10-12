def gldas_variables():
    """
    List of the plottable variables from the GLDAS 2.1 datasets used
    """
    variables = {
        'Air Temperature': 'Tair_f_inst',
        'Surface Albedo': 'Albedo_inst',
        'Surface Temperature': 'AvgSurfT_inst',
        'Canopy Water Amount': 'CanopInt_inst',
        'Evaporation Flux From Canopy': 'ECanop_tavg',
        'Evaporation Flux From Soil': 'ESoil_tavg',
        'Water Evaporation Flux': 'Evap_tavg',
        'Surface Downwelling Longwave Flux In Air': 'LWdown_f_tavg',
        'Surface Net Downward Longwave Flux': 'Lwnet_tavg',
        'Potential Evaporation Flux': 'PotEvap_tavg',
        'Surface Air Pressure': 'Psurf_f_inst',
        'Specific Humidity': 'Qair_f_inst',
        'Downward Heat Flux In Soil': 'Qg_tavg',
        'Surface Upward Sensible Heat Flux': 'Qh_tavg',
        'Surface Upward Latent Heat Flux': 'Qle_tavg',
        'Surface Runoff Amount': 'Qs_acc',
        'Subsurface Runoff Amount': 'Qsb_acc',
        'Surface Snow Melt Amount': 'Qsm_acc',
        'Precipitation Flux': 'Rainf_f_tavg',
        'Rainfall Flux': 'Rainf_tavg',
        'Root Zone Soil Moisture': 'RootMoist_inst',
        'Surface Snow Amount': 'SWE_inst',
        'Soil Temperature': 'SoilTMP0_10cm_inst',
        'Surface Downwelling Shortwave Flux In Air': 'SWdown_f_tavg',
        'Surface Snow Thickness': 'SnowDepth_inst',
        'Snowfall Flux': 'Snowf_tavg',
        'Surface Net Downward Shortwave Flux': 'Swnet_tavg',
        'Transpiration Flux From Veg': 'Tveg_tavg',
        'Wind Speed': 'Wind_f_inst',
        # 'Latitude': 'lat',
        # 'Longitude': 'lon',
        # 'Time': 'time',
        }
    return variables


def wms_colors():
    """
    Color options usable by thredds wms
    """
    color_opts = [
        ('SST-36', 'sst_36'),
        ('Greyscale', 'greyscale'),
        ('Rainbox', 'rainbow'),
        ('OCCAM', 'occam'),
        ('OCCAM Pastel', 'occam_pastel-30'),
        ('Red-Blue', 'redblue'),
        ('NetCDF Viewer', 'ncview'),
        ('ALG', 'alg'),
        ('ALG 2', 'alg2'),
        ('Ferret', 'ferret'),
        # ('Probability', 'prob'),
        # ('White-Blue', whiteblue'),
        # ('Grace', 'grace'),
        ]
    return color_opts


def get_times():
    """
    Time intervals of GLDAS data
    """
    import os
    times = [
        (2000, 2000),
        (2001, 2001),
        (2002, 2002),
        (2003, 2003),
        (2004, 2004),
        (2005, 2005),
        (2006, 2006),
        (2007, 2007),
        (2008, 2008),
        (2009, 2009),
        (2010, 2010),
        (2011, 2011),
        (2012, 2012),
        (2013, 2013),
        (2014, 2014),
        (2015, 2015),
        (2016, 2016),
        (2017, 2017),
        (2018, 2018),
    ]
    dir = '/home/rchales/thredds/gldas/preprocessed_yrs'
    years = os.listdir(dir)
    years.sort()
    for year in years:
        times.append((year, year))
    return times