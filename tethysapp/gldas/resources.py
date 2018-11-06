from .app import Gldas, CustomSetting
import os

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
    times = [
        (2018, 2018),
        (2017, 2017),
        (2016, 2016),
        (2015, 2015),
        (2014, 2014),
        (2013, 2013),
        (2012, 2012),
        (2011, 2011),
        (2010, 2010),
        (2009, 2009),
        (2008, 2008),
        (2007, 2007),
        (2006, 2006),
        (2005, 2005),
        (2004, 2004),
        (2003, 2003),
        (2002, 2002),
        (2001, 2001),
        (2000, 2000),
        ('All Available Times', 'alltimes'),
    ]
    return times

def get_zooms():
    """
    List of places to zoom to and their [lat, long, zoom]
    """
    zooms = [
        ('Full Extent', 'Full Extent'),
        ('North America', 'North America'),
        ('South America', 'South America'),
        ('Europe', 'Europe'),
        ('Africa', 'Africa'),
        ('Asia', 'Asia'),
        ('Australia', 'Australia'),
    ]
    return zooms

def app_configuration():
    app_workspace = Gldas.get_app_workspace()
    app_wksp_path = os.path.join(app_workspace.path, '')
    thredds_wms_url = Gldas.get_custom_setting("Thredds WMS URL")
    thredds_data_dir = Gldas.get_custom_setting("Local Thredds Folder Path")
    viewID = Gldas.get_custom_setting("Google Analytics Tracking: View ID")

    settings = {
        'app_wksp_path': app_wksp_path,
        'thredds_wms_url': thredds_wms_url,
        'thredds_data_dir': thredds_data_dir,
        'viewID': viewID,
    }

    return settings

def GAmetrics():
    metrics = [
        ('Total Uses', 'ga:sessions'),
        # ('Users Last 30 Days', 'ga:30dayUsers'),
        # ('Average Session Duration', 'ga:avgSessionDuration'),
        # ('User Countries', 'ga:country'),
        # ('User Cities', 'ga:city'),
    ]

    return metrics
