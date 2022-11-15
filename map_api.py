import folium
from tracker import *
import webbrowser
from fastapi import FastAPI

app = FastAPI()

def createMap(starting_coords): #creates the map
    mapping = folium.Map(location=starting_coords, zoom_start=20)

    tile = folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri Satellite',
        overlay=False,
        control=True
    ).add_to(mapping)

    return mapping

def openMap(tracker): #adds each detection to map
    detections_list = tracker.detections_list
    for det in detections_list:
        det.addPoint()

    webbrowser.open("map.html")

#add detection with info to map (from cache or db?) (maybe have buttons for both or chance to see Fod over week) 
#make detection point clickable
#Edit detection values
#open map