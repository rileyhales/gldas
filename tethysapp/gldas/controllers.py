from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import SelectInput, RangeSlider
from .options import gldas_variables, wms_colors, geojson_colors, timecoverage, get_charttypes
from .app import Gldas as App


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    variables = gldas_variables()
    options = []
    for key in sorted(variables.keys()):
        tuple1 = (key, variables[key])
        options.append(tuple1)
    del tuple1, key, variables

    variables = SelectInput(
        display_text='Select GLDAS Variable',
        name='variables',
        multiple=False,
        original=True,
        options=options,
    )

    dates = SelectInput(
        display_text='Time Interval',
        name='dates',
        multiple=False,
        original=True,
        options=timecoverage(),
        initial='alltimes'
    )

    colorscheme = SelectInput(
        display_text='Raster Color Scheme',
        name='colorscheme',
        multiple=False,
        original=True,
        options=wms_colors(),
        initial='rainbow'
    )

    opacity = RangeSlider(
        display_text='Raster Opacity',
        name='opacity',
        min=.5,
        max=1,
        step=.05,
        initial=1,
    )

    gj_color = SelectInput(
        display_text='Boundary - Border Colors',
        name='gjColor',
        multiple=False,
        original=True,
        options=geojson_colors(),
        initial='#ffffff'
    )

    gj_opacity = RangeSlider(
        display_text='Boundary - Border Opacity',
        name='gjOpacity',
        min=0,
        max=1,
        step=.1,
        initial=1,
    )

    gj_weight = RangeSlider(
        display_text='Boundary - Border Thickness',
        name='gjWeight',
        min=1,
        max=5,
        step=1,
        initial=2,
    )

    gj_fillcolor = SelectInput(
        display_text='Boundary - Fill Colors',
        name='gjFillColor',
        multiple=False,
        original=True,
        options=geojson_colors(),
        initial='rgb(0,0,0,0)'
    )

    gj_fillopacity = RangeSlider(
        display_text='Boundary - Fill Opacity',
        name='gjFillOpacity',
        min=0,
        max=1,
        step=.1,
        initial=.5,
    )

    charttype = SelectInput(
        display_text='Choose a Plot Type',
        name='charttype',
        multiple=False,
        original=True,
        options=get_charttypes(),
    )

    context = {
        # data options
        'variables': variables,
        'dates': dates,
        # display options
        'colorscheme': colorscheme,
        'opacity': opacity,
        'gjColor': gj_color,
        'gjOpacity': gj_opacity,
        'gjWeight': gj_weight,
        'gjFillColor': gj_fillcolor,
        'gjFillOpacity': gj_fillopacity,
        'charttype': charttype,
        # metadata
        'youtubelink': App.youtubelink,
        'githublink': App.githublink,
        'gldaslink': App.gldaslink,
        'version': App.version,
    }

    return render(request, 'gldas/home.html', context)
