def gldas_variables():
    """
    List of the plottable variables from the GLDAS 2.1 datasets used
    """
    return [('Air Temperature', 'Tair_f_inst'),
            ('Canopy Water Amount', 'CanopInt_inst'),
            ('Downward Heat Flux In Soil', 'Qg_tavg'),
            ('Evaporation Flux From Canopy', 'ECanop_tavg'),
            ('Evaporation Flux From Soil', 'ESoil_tavg'),
            ('Potential Evaporation Flux', 'PotEvap_tavg'),
            ('Precipitation Flux', 'Rainf_f_tavg'),
            ('Rainfall Flux', 'Rainf_tavg'),
            ('Root Zone Soil Moisture', 'RootMoist_inst'),
            ('Snowfall Flux', 'Snowf_tavg'),
            ('Soil Temperature', 'SoilTMP0_10cm_inst'),
            ('Specific Humidity', 'Qair_f_inst'),
            ('Subsurface Runoff Amount', 'Qsb_acc'),
            ('Surface Air Pressure', 'Psurf_f_inst'),
            ('Surface Albedo', 'Albedo_inst'),
            ('Surface Downwelling Longwave Flux In Air', 'LWdown_f_tavg'),
            ('Surface Downwelling Shortwave Flux In Air', 'SWdown_f_tavg'),
            ('Surface Net Downward Longwave Flux', 'Lwnet_tavg'),
            ('Surface Net Downward Shortwave Flux', 'Swnet_tavg'),
            ('Surface Runoff Amount', 'Qs_acc'),
            ('Surface Snow Amount', 'SWE_inst'),
            ('Surface Snow Melt Amount', 'Qsm_acc'),
            ('Surface Snow Thickness', 'SnowDepth_inst'),
            ('Surface Temperature', 'AvgSurfT_inst'),
            ('Surface Upward Latent Heat Flux', 'Qle_tavg'),
            ('Surface Upward Sensible Heat Flux', 'Qh_tavg'),
            ('Transpiration Flux From Veg', 'Tveg_tavg'),
            ('Water Evaporation Flux', 'Evap_tavg'),
            ('Wind Speed', 'Wind_f_inst')]


def timeintervals():
    """
    Time intervals of GLDAS data
    """
    return [
        ('All Available Times', 'alltimes'),
        ('2010s', '2010s'),
        ('2000s', '2000s'),
        ('1990s', '1990s'),
        ('1980s', '1980s'),
        ('1970s', '1970s'),
        ('1960s', '1960s'),
        ('1950s', '1950s'),
    ]


def wms_colors():
    """
    Color options usable by thredds wms
    """
    return [
        ('SST-36', 'sst_36'),
        ('Greyscale', 'greyscale'),
        ('Rainbow', 'rainbow'),
        ('OCCAM', 'occam'),
        ('OCCAM Pastel', 'occam_pastel-30'),
        ('Red-Blue', 'redblue'),
        ('NetCDF Viewer', 'ncview'),
        ('ALG', 'alg'),
        ('ALG 2', 'alg2'),
        ('Ferret', 'ferret'),
        ]


def geojson_colors():
    return [
        ('White', '#ffffff'),
        ('Transparent', 'rgb(0,0,0,0)'),
        ('Red', '#ff0000'),
        ('Green', '#00ff00'),
        ('Blue', '#0000ff'),
        ('Black', '#000000'),
        ('Pink', '#ff69b4'),
        ('Orange', '#ffa500'),
        ('Teal', '#008080'),
        ('Purple', '#800080'),
    ]


def get_charttypes():
    return [
        ('Full Timeseries (Single-Line Plot)', 'timeseries'),
        ('Monthly Analysis (Box Plot)', 'monthbox'),
        ('Monthly Analysis (Multi-Line Plot)', 'monthmulti'),
        ('Yearly Analysis (Box Plot)', 'yearbox'),
        ('Yearly Analysis (Multi-Line Plot)', 'yearmulti'),
    ]


def worldregions():
    """
    Populates the drop down menu with the list of available shapefiles to use for averaging
    Dependencies: os, App (app)
    """
    return (
        ('All World Regions (ESRI Living Atlas)', ''),
        ('Antarctica (ESRI Living Atlas)', 'Antarctica'),
        ('Asiatic Russia (ESRI Living Atlas)', 'Asiatic Russia'),
        ('Australia/New Zealand (ESRI Living Atlas)', 'Australia/New Zealand'),
        ('Caribbean (ESRI Living Atlas)', 'Caribbean'),
        ('Central America (ESRI Living Atlas)', 'Central America'),
        ('Central Asia (ESRI Living Atlas)', 'Central Asia'),
        ('Eastern Africa (ESRI Living Atlas)', 'Eastern Africa'),
        ('Eastern Asia (ESRI Living Atlas)', 'Eastern Asia'),
        ('Eastern Europe (ESRI Living Atlas)', 'Eastern Europe'),
        ('European Russia (ESRI Living Atlas)', 'European Russia'),
        ('Melanesia (ESRI Living Atlas)', 'Melanesia'),
        ('Micronesia (ESRI Living Atlas)', 'Micronesia'),
        ('Middle Africa (ESRI Living Atlas)', 'Middle Africa'),
        ('Northern Africa (ESRI Living Atlas)', 'Northern Africa'),
        ('Northern America (ESRI Living Atlas)', 'Northern America'),
        ('Northern Europe (ESRI Living Atlas)', 'Northern Europe'),
        ('Polynesia (ESRI Living Atlas)', 'Polynesia'),
        ('South America (ESRI Living Atlas)', 'South America'),
        ('Southeastern Asia (ESRI Living Atlas)', 'Southeastern Asia'),
        ('Southern Africa (ESRI Living Atlas)', 'Southern Africa'),
        ('Southern Asia (ESRI Living Atlas)', 'Southern Asia'),
        ('Southern Europe (ESRI Living Atlas)', 'Southern Europe'),
        ('Western Africa (ESRI Living Atlas)', 'Western Africa'),
        ('Western Asia (ESRI Living Atlas)', 'Western Asia'),
        ('Western Europe (ESRI Living Atlas)', 'Western Europe'),
        ('None', 'none')
    )
