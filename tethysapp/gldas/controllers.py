from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import SelectInput, RangeSlider
from .model import gldas_variables, wms_colors, get_times
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

    updated = App.updated
    youtubelink = App.youtubelink
    gldaslink = App.gldaslink

    variables = SelectInput(
        display_text='Select GLDAS Variable',
        name='variables',
        multiple=False,
        original=True,
        options=options,
    )

    colors = SelectInput(
        display_text='Color Scheme',
        name='colors',
        multiple=False,
        options=wms_colors(),
    )

    dates = SelectInput(
        display_text='Time Interval',
        name='dates',
        multiple=False,
        options=get_times(),
    )

    opacity = RangeSlider(
        display_text='Layer Opacity',
        name='opacity',
        min=.4,
        max=1,
        step=.05,
        initial=.8,
    )

    context = {
        'variables': variables,
        'opacity': opacity,
        'colors': colors,
        'dates': dates,
        'youtubelink': youtubelink,
        'gldaslink': gldaslink,
        'updated': updated,
    }

    return render(request, 'gldas/home.html', context)