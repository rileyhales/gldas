from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import SelectInput, RangeSlider
from .model import gldas_variables, wms_colors, geojson_colors, timecoverage, worldregions, get_charttypes
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

    colorscheme = SelectInput(
        display_text='Raster Color Scheme',
        name='colorscheme',
        multiple=False,
        original=True,
        options=wms_colors(),
        initial='rainbow'
    )

    dates = SelectInput(
        display_text='Time Interval',
        name='dates',
        multiple=False,
        original=True,
        options=timecoverage(),
        initial='alltimes'
    )

    regions = SelectInput(
        display_text='World Regions',
        name='regions',
        multiple=False,
        original=True,
        options=worldregions(),
    )

    opacity_raster = RangeSlider(
        display_text='Raster Opacity',
        name='opacity_raster',
        min=.5,
        max=1,
        step=.05,
        initial=.8,
    )

    colors_geojson = SelectInput(
        display_text='Boundary Colors',
        name='colors_geojson',
        multiple=False,
        original=True,
        options=geojson_colors(),
        initial='#ffffff'
    )

    opacity_geojson = RangeSlider(
        display_text='Boundary Opacity',
        name='opacity_geojson',
        min=.0,
        max=1,
        step=.05,
        initial=.25,
    )

    charttype = SelectInput(
        display_text='Choose a Plot Type',
        name='charttype',
        multiple=False,
        original=True,
        options=get_charttypes(),
    )

    context = {
        'variables': variables,
        'opacity_raster': opacity_raster,
        'colorscheme': colorscheme,
        'dates': dates,
        'regions': regions,
        'opacity_geojson': opacity_geojson,
        'colors_geojson': colors_geojson,
        'charttype': charttype,
        'youtubelink': App.youtubelink,
        'githublink': App.githublink,
        'gldaslink': App.gldaslink,
        'version': App.version,
    }

    return render(request, 'gldas/home.html', context)
