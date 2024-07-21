import json
import math
import time
import geocoder
import pandas as pd
import folium
from folium.plugins import Fullscreen, LocateControl, Geocoder

def renderMap(lat, long):
    
    print("Coordinates:", lat, long)
    start = time.time()
    area, confidence, polygon = get_building_data(lat, long)
    end = time.time()
    print("Time taken:", end-start)
    print("Area:", area, "Confidence:", confidence)
            
    map = folium.Map(
        tiles='cartodbdark_matter',
        location=[lat, long],
        zoom_start=18
    )
        
    polygon_coords = read_polygon(polygon)
    
    folium.Polygon(locations=polygon_coords, color='yellow', weight=2, fill=True, fill_color='orange').add_to(map)

    folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = False,
        control = True
       ).add_to(map)
    
    folium.LayerControl(position='bottomright').add_to(map)
    Fullscreen().add_to(map)
    LocateControl().add_to(map)
    Geocoder().add_to(map)
    folium.LatLngPopup().add_to(map)

    map = map._repr_html_()

    context = {'map': map}

    return context

def read_polygon(polygon_str): 
    cleaned_str = polygon_str.replace("POLYGON((", "").replace("))", "")
    
    coordinate_pairs = cleaned_str.split(", ")
    
    polygon_coords = [
        (float(lat), float(long)) for long, lat in (pair.split() for pair in coordinate_pairs)
    ]
    
    return polygon_coords
    


def geocode(text):
    g = geocoder.google(text)
    return g.latlng

def find_file_number(lat, long):
    file_dir = 'solar_calculator/data/metadata.json'
    with open(file_dir, 'r') as f:
        data = json.load(f)
    
    for key, val in data.items():
        minLat, maxLat = val['minLat'], val['maxLat']
        minLong, maxLong = val['minLong'], val['maxLong']
        if minLat <= lat <= maxLat and minLong <= long <= maxLong:
            return key

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def get_building_data(lat, long):
    file_num = find_file_number(lat, long)
    file_name = f"smaller_file_part_{file_num}.csv"
    df = pd.read_csv(f'solar_calculator/data/{file_name}')
    
    selected_row = df.loc[(df['latitude'] == lat) & (df['longitude'] == long)]
    
    if not selected_row.empty:
        area = selected_row.iloc[0]['area_in_meters']
        confidence = selected_row.iloc[0]['confidence']
        polygon = selected_row.iloc[0]['geometry']
    
    else:
        df['distance'] = df.apply(lambda row: haversine(lat, long, row['latitude'], row['longitude']), axis=1)
        closest_row = df.loc[df['distance'].idxmin()]
        area = closest_row['area_in_meters']
        confidence = closest_row['confidence']
        polygon = closest_row['geometry']
        
    return area, confidence, polygon
    
    
