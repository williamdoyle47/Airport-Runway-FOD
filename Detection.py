import base64
import folium
from folium import IFrame
import random
from gps_controller import *
import datetime
import sqlite3

class Detection:

    staticId = 1

    def __init__(self, fod_type, mapping, gps_controller):
        self.gps_controller = gps_controller
        self.fod_type = fod_type
        self.point = self.get_position()
        self.mapping = mapping
        self.id = self.staticId
        Detection.staticId += 1
        self.image = "detectionImages/" + str(self.id) + ".jpeg"
        print("Detection object created at coordinates: " + str(self.point))
        

    def addPoint(self):
        if self.point: # If point is defined
            width = 500
            height = 500
            encoded = base64.b64encode(open(self.image, 'rb').read())
            html = '<img src="data:image/png;base64, {}" style="height:100%;width:100%;">'.format
            iframe = IFrame(html(encoded.decode('UTF-8'), width, height))
            popup = folium.Popup(iframe, min_width=1000, max_width=2650)
            folium.Marker(self.point, popup=popup).add_to(self.m)
            self.mapping.save("map.html")

    # For simulating fake GPS coordinates (ECC parking lot)
    def get_position_simulated(self):
        lat = random.uniform(45.54968462694988, 45.55057682445797)
        long = random.uniform(-94.15178127548012, -94.15303386704261)
        return [lat, long]

    # For getting real coordinates from GPS device
    def get_position(self):
        try:
            #coords = self.gps_controller.extract_coordinates()
            coords = self.gps_controller.last_coords
            return coords
        except:
            return None

    def writeToLog(self):
        with open("Log.txt", "a") as text_file:
            text_file.write("Object detected at: " + str(self.point) + '\n')

    def insertToDb(self):
        try:
            conn = sqlite3.connect('detections.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO detections VALUES (?, ?, ?)", (self.fod_type, str(self.get_position()),
            datetime.datetime.now()))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(e)


# Testing (only executes if this file is run directly)
if __name__ == "__main__":

    gps_controller = GPS_Controller()
    mapping = folium.Map(location=[45.550120, -94.152411], zoom_start=20)

    tile = folium.TileLayer(
            tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr = 'Esri',
            name = 'Esri Satellite',
            overlay = False,
            control = True
        ).add_to(mapping)

    det1 = Detection("wood", mapping, gps_controller)
    det2 = Detection("wood", mapping, gps_controller)
    det3 = Detection("wood", mapping, gps_controller)
    print(det1.id)
    print(det2.id)
    print(det3.id)
    mapping.save("map.html")

    print(det1.get_position())