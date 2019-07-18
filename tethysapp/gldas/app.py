from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting


class Gldas(TethysAppBase):
    """
    Tethys app class for GLDAS Data Visualizer.
    """

    name = 'GLDAS Data Tool'
    index = 'gldas:home'
    icon = 'gldas/images/globe.png'
    package = 'gldas'
    root_url = 'gldas'
    color = '#002366'
    description = 'Visualizes NASA GLDAS monthly data with time animated maps.\n' \
                  'Generates timeseries charts and datasets at points or averaged over polygons.\n' \
                  'Perform simple statistical analysis on historical data by month and year.'
    tags = 'NASA, GLDAS, Timeseries'
    enable_feedback = False
    feedback_emails = []
    githublink = 'https://github.com/rileyhales/gldas'
    datawebsite = 'https://disc.gsfc.nasa.gov/datasets/GLDAS_NOAH025_M_V2.1/summary?keywords=gldas'
    version = 'v3 Jul19'

    def url_maps(self):
        """
        Add controllers
        """
        urlmap = url_map_maker(self.root_url)

        url_maps = (
            # url maps to navigable pages
            urlmap(
                name='home',
                url='gldas',
                controller='gldas.controllers.home'
            ),

            # url maps for ajax calls
            urlmap(
                name='getChart',
                url='gldas/ajax/getChart',
                controller='gldas.ajax.getchart',
            ),
            urlmap(
                name='uploadShapefile',
                url='gldas/ajax/uploadShapefile',
                controller='gldas.ajax.uploadshapefile',
            ),

            # url maps for api calls
            urlmap(
                name='getcapabilities',
                url='gldas/api/getcapabilities',
                controller='gldas.api.getcapabilities',
            ),
            urlmap(
                name='timeseries',
                url='gldas/api/timeseries',
                controller='gldas.api.timeseries',
            ),
            urlmap(
                name='gldasvariables',
                url='gldas/api/gldasvariables',
                controller='gldas.api.gldasvariables',
            ),
            urlmap(
                name='gldasdates',
                url='gldas/api/gldasdates',
                controller='gldas.api.gldasdates',
            ),

        )
        return url_maps

    def custom_settings(self):
        custom_settings = (
            CustomSetting(
                name='Local Thredds Folder Path',
                type=CustomSetting.TYPE_STRING,
                description="Local file path to datasets (same as used by Thredds) (e.g. /home/thredds/myDataFolder/)",
                required=True,
            ),
            CustomSetting(
                name='Thredds WMS URL',
                type=CustomSetting.TYPE_STRING,
                description="URL to the GLDAS folder on the thredds server (e.g. http://[host]/thredds/gldas/)",
                required=True,
            ),
            CustomSetting(
                name='GeoserverURL',
                type=CustomSetting.TYPE_STRING,
                description="Include http or https but no '/' after /geoserver, ex: https://tethys.byu.edu/geoserver",
                required=False,
            ),
            CustomSetting(
                name='Geoserver user/pass',
                type=CustomSetting.TYPE_STRING,
                description="Admin credentials for uploading shapefiles to geoserver in the format username/password",
                required=False,
            ),
        )
        return custom_settings
