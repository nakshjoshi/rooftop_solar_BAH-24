from django.shortcuts import render
from django.http import HttpResponse
from .forms import DataForm

def home(request):
    return render(request, 'solar_calculator/home.html')

def process_data(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            lat = form.cleaned_data['latitude']
            long = form.cleaned_data['longitude']
            
            return HttpResponse('/success/')
        else:
            form = DataForm()
            
    return render(request, 'solar_calculator/results.html', {'form': form})
