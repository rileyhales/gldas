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
    color = '#ace9e7'
    description = 'Visualizes GLDAS data through maps and charts'
    tags = '&quot;NASA&quot;, &quot;GLDAS&quot;, &quot;LDAS&quot;, &quot;charts&quot;, &quot;maps&quot;, &quot;teries&quot;'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        # url maps to navigable pages
        url_maps = (
            UrlMap(
                name='home',
                url='gldas',
                controller='gldas.controllers.home'
            ),

        # url maps for ajax calls
            UrlMap(
                name='generatePlot',
                url='gldas/generatePlot',
                controller='gldas.ajaxhandlers.generatePlot',
            ),
            UrlMap(
                name='getBounds',
                url='gldas/getBounds',
                controller='gldas.ajaxhandlers.getBounds',
            ),
            UrlMap(
                name='getPaths',
                url='gldas/getPaths',
                controller='gldas.ajaxhandlers.getPaths'
            ),

        # url map for api calls
            UrlMap(
                name='tsPlotValues',
                url='gldas/api/tsPlotValues',
                controller='gldas.api.tsPlotValues',
            ),
            UrlMap(
                name='getTimes',
                url='gldas/api/getTimes',
                controller='gldas.api.getTimes',
            ),
        )
        return url_maps

    def custom_settings(self):
        CustomSettings = (
            CustomSetting(
                name='Local Thredds Folder Path',
                type=CustomSetting.TYPE_STRING,
                description="Path to data in the folder mounted by Thredds",
                required=True,
                # /home/rchales/thredds/gldas/
            ),
            CustomSetting(
                name='Thredds Base URL',
                type=CustomSetting.TYPE_STRING,
                description="URL to the Thredds catalog (e.g. tethys.byu.edu/thredds/)",
                required=True,
                # http://127.0.0.1:7000/thredds/
            ),
        )
        return CustomSettings
