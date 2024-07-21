from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.contrib import messages
import folium
from folium.plugins import Fullscreen, LocateControl, Geocoder

from .models import Feature
from .utils import basemap


def index(request):
    map = basemap(request)
    return render(request, 'map.html', map)

