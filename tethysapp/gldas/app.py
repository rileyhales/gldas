from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting, SpatialDatasetServiceSetting


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
    docslink = 'https://gldas-data-tool.readthedocs.io/en/latest/index.html'
    datawebsite = 'https://disc.gsfc.nasa.gov/datasets/GLDAS_NOAH025_M_V2.1/summary?keywords=gldas'
    version = 'v4 Feb20'

    def url_maps(self):
        """
        Add controllers
        """
        urlmap = url_map_maker(self.root_url)

        return (
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
            urlmap(
                name='uploadGeoJSON',
                url='gldas/ajax/uploadGeoJSON',
                controller='gldas.ajax.uploadgeojson',
            ),

            # url maps for api calls
            urlmap(
                name='helpme',
                url='gldas/api/help',
                controller='gldas.api.helpme',
            ),
            urlmap(
                name='timeseries',
                url='gldas/api/timeseries',
                controller='gldas.api.timeseries',
            ),
        )

    def custom_settings(self):
        return (
            CustomSetting(
                name='thredds_path',
                type=CustomSetting.TYPE_STRING,
                description="Local file path to datasets (same as used by Thredds) (e.g. /home/thredds/myDataFolder/)",
                required=True,
                default='/Users/rileyhales/thredds/gldas/',
            ),
            CustomSetting(
                name='thredds_url',
                type=CustomSetting.TYPE_STRING,
                description="URL to the GLDAS folder on the thredds server (e.g. http://[host]/thredds/gldas/)",
                required=True,
                default='https://tethys2.byu.edu/thredds/wms/testAll/gldas/',
            )
        )

    def spatial_dataset_service_settings(self):
        return (
            SpatialDatasetServiceSetting(
                name='geoserver',
                description='Geoserver for serving user uploaded shapefiles',
                engine=SpatialDatasetServiceSetting.GEOSERVER,
                required=True,
            ),
        )
