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
    description = 'Visualizes GLDAS data through maps and charts'
    tags = '&quot;NASA&quot;, &quot;GLDAS&quot;, &quot;LDAS&quot;, &quot;charts&quot;, &quot;maps&quot;, &quot;tseries&quot;'
    enable_feedback = False
    feedback_emails = []
    updated = '1 April 2019'
    youtubelink = 'https://www.youtube.com/channel/UC6B62KhB-Cd34ad6pGBldQQ/videos'
    gldaslink = 'https://disc.gsfc.nasa.gov/datasets/GLDAS_NOAH025_M_V2.1/summary?keywords=gldas'

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
                url='gldas/ajax/generatePlot',
                controller='gldas.ajax.generatePlot',
            ),
            UrlMap(
                name='getBounds',
                url='gldas/ajax/getBounds',
                controller='gldas.ajax.getBounds',
            ),
            UrlMap(
                name='customsettings',
                url='gldas/ajax/customsettings',
                controller='gldas.ajax.customsettings'
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
                description="Path to data in the folder mounted by Thredds (e.g. /home/thredds/myDataFolder/)",
                required=True,
                # /home/rchales/thredds/gldas/
            ),
            CustomSetting(
                name='Thredds WMS URL',
                type=CustomSetting.TYPE_STRING,
                description="URL to the folder of GLDAS data and .ncml files on the thredds server (e.g. tethys.byu.edu/thredds/myDataFolder/)",
                required=True,
                # http://127.0.0.1:7000/thredds/wms/testAll/
            ),
        )
        return CustomSettings
