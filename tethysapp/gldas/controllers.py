from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import SelectInput, RangeSlider
from .resources import gldas_variables, wms_colors, get_times

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

    layers = SelectInput(
        display_text='Select GLDAS Variable',
        name='layers',
        multiple=False,
        original=True,
        options=options,
    )

    colors = SelectInput(
        display_text='Color Scheme',
        name='colors',
        multiple=False,
        original=True,
        options=wms_colors(),
    )

    times = SelectInput(
        display_text='Time Intervals',
        name='times',
        multiple=False,
        original=True,
        options=get_times(),
    )

    opacity = RangeSlider(
        display_text='Layer Opacity',
        name='opacity',
        min=0,
        max=1,
        step=.05,
        initial=.7,
    )

    context = {
        'layers': layers,
        'opacity': opacity,
        'colors': colors,
        'times': times,
    }

    return render(request, 'gldas/home.html', context)