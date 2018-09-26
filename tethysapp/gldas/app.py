from tethys_sdk.base import TethysAppBase, url_map_maker


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
                controller='gldas.ajaxhandlers.generatePlot'
            ),

        )

        return url_maps
