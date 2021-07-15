from typing import Match
from django.shortcuts import render, redirect
import os
import pandas as pd
import geopandas as gpd
import osmnx
import folium
from folium.plugins import MousePosition
import matplotlib.pyplot as plt
import seaborn as sb

# Create your views here.
def home(request):

    map = folium.Map([13.1031, 80.1794], zoom_start=10, tiles="CartoDb dark_matter")
    map.add_child(folium.ClickForMarker())
    MousePosition().add_to(map)
    from folium.plugins import MiniMap
    MiniMap(tile_layer='Stamen WaterColor', position='bottomleft').add_to(map)

    ## exporting
    map=map._repr_html_()
    context = {'my_map': map}

    ## rendering
    return render(request,'geoApp/home.html',context)

def streetmap(request):

    place = "Chennai, India"
    graph = osmnx.graph.graph_from_place(place, network_type='drive')
    #osmnx.io.save_graph_shapefile(graph) 

    nodes, streets = osmnx.graph_to_gdfs(graph) 

    street_types = pd.DataFrame(streets["highway"].apply(pd.Series)[0].value_counts().reset_index())
    street_types.columns = ["type", "count"]

    style = {'color': '#F7DC6F', 'weight':'1'}
    m = folium.Map([13.1031, 80.1794],zoom_start=15,tiles="CartoDb positron")
    folium.GeoJson(streets, style_function=lambda x: style).add_to(m)
    folium.GeoJsonTooltip(fields=['name'])
    # m.save("streets.html")

    ## exporting
    m=m._repr_html_()
    context = {'my_map': m}

    return render(request, 'geoApp/home.html', context)


def hospitals(request):

    place = "Chennai, India"
    hospitals = osmnx.geometries.geometries_from_place(place, {'amenity':'hospital'})
    hospital_points = hospitals[hospitals.geom_type == "Point"]

    
    m = folium.Map([13.1031, 80.1794], zoom_start=10, tiles="CartoDb dark_matter")
    locs = zip(hospital_points.geometry.y, hospital_points.geometry.x)
    for location in locs:
        folium.CircleMarker(location=location, popup=folium.Popup(location) , color = "#F4F6F6",   radius=2).add_to(m)
    # m.save("hospitals.html")

    ## exporting
    m=m._repr_html_()
    context = {'my_map': m}

    return render(request, 'geoApp/home.html', context)



def buildings(request):

    place = "Chennai, India"
    buildings = osmnx.geometries.geometries_from_place(place, {'building': True})
    buildings["amenity"].apply(pd.Series)[0].value_counts()

    
    style_buildings = {'color':'#6C3483 ', 'fillColor': '#6C3483 ', 'weight':'1', 'fillOpacity' : 1}

    m = folium.Map([13.1031, 80.1794],
               zoom_start=15,
               tiles="cartoDb positron")

    buildingJson = folium.GeoJson(buildings[:1000], style_function=lambda x: style_buildings).add_to(m)
    folium.GeoJsonTooltip(fields=['name','amenity'], labels=False).add_to(buildingJson)
    # m.save("buildings.html")
    m

    ## exporting
    m=m._repr_html_()
    context = {'my_map': m}

    return render(request, 'geoApp/home.html', context)