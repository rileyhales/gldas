from tethys_sdk.base import TethysAppBase, url_map_maker

# todo: make a global variable for base thredds url and the path to the data. needs to work in python, js, html
# todo: make the legend rescale itself automatically based on max/min values
# todo: fix the appearance of the legend on the right side of the map

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
