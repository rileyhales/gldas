from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import SelectInput, RangeSlider, Button
from .resources import gldas_variables

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    variables = gldas_variables()
    options = [('All Variables', 'allvars')]
    for key in sorted(variables.keys()):
        tuple1 = (key, variables[key])
        options.append(tuple1)

    select_input = SelectInput(
        display_text='Select Variable',
        name='select1',
        multiple=False,
        original=True,
        options=options,
        initial=['All Variables'],
    )

    range_slider = RangeSlider(
        display_text='Layer Opacity',
        name='slider1',
        min=0,
        max=1,
        step=.05,
        initial=.7,
    )

    context = {
        'select_input': select_input,
        'range_slider': range_slider,
    }

    return render(request, 'gldas/home.html', context)