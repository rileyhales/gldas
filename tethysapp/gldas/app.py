from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting


class Gldas(TethysAppBase):
    """
    Tethys app class for GLDAS Data Visualizer.
    """

    name = 'GLDAS Data Visualizer'
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
    youtubelink = 'https://youtu.be/GJCu70jQfwU'
    githublink = 'https://github.com/rileyhales/gldas'
    gldaslink = 'https://disc.gsfc.nasa.gov/datasets/GLDAS_NOAH025_M_V2.1/summary?keywords=gldas'
    version = 'Version 2.7.3 - 5 June 2019'

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
                name='getCustomSettings',
                url='gldas/ajax/getCustomSettings',
                controller='gldas.ajax.get_customsettings'
            ),
            urlmap(
                name='getPointSeries',
                url='gldas/ajax/getPointSeries',
                controller='gldas.ajax.get_pointseries',
            ),
            urlmap(
                name='getPolygonAverage',
                url='gldas/ajax/getPolygonAverage',
                controller='gldas.ajax.get_polygonaverage',
            ),
            urlmap(
                name='getShapeAverage',
                url='gldas/ajax/getShapeAverage',
                controller='gldas.ajax.get_shapeaverage',
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
                name='Geoserver Workspace URL',
                type=CustomSetting.TYPE_STRING,
                description="URL (wfs) of the workspace on geoserver (e.g. https://[host]/geoserver/gldas/ows). \n"
                            "Enter geojson instead of a url if you experience GeoServer problems.",
                required=True,
            ),
        )
        return custom_settings
