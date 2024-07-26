from django.shortcuts import render

import solar_calculator.utils as utils
from .forms import DataForm


def index(request):
    return render(request, 'home.html')

def process_data(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            lat = form.cleaned_data['latitude']
            long = form.cleaned_data['longitude']
            
            # TODO: Fix error here
            if not (lat or long):
                lat, long = utils.geocode(address)
                print(lat, long)
            
            
        else:
            form = DataForm()
    
    map = utils.renderMap(float(lat), float(long))
    
    return render(request, 'result.html', map)
