import time
from django.shortcuts import render
from django.http import HttpResponse
from .forms import DataForm

import solar_calculator.utils as utils

def home(request):
    return render(request, 'solar_calculator/home.html')

def process_data(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            lat = float(form.cleaned_data['latitude'])
            long = float(form.cleaned_data['longitude'])
            
            # TODO: Fix error here
            if not (lat or long):
                lat, long = utils.geocode(address)
                print(lat, long)
            
            start = time.time()
            area, confidence = utils.get_building_data(lat, long)
            end = time.time()
            print(end-start)
            print(area, confidence)
            
            
        else:
            form = DataForm()
            
    return render(request, 'solar_calculator/results.html', {'form': form})
