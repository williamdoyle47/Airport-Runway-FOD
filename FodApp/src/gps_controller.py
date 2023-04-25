# This script is used for extracting the coordinates from the raw data of the GPS puck.
import socket
import serial
from logging import exception
from pyembedded.gps_module.gps import GPS
import os
import folium
from folium import IFrame

# class NoGPSError(Exception):
#     print("No Device Found")
#     pass


class GPS_Controller():

    last_coords = None

    def __init__(self) -> None:
        self.gps = self.get_gps_device()

    def get_gps_device(self):
        numof_ports_searched = 30
        gps = None
        print("\nSearching for GPS on your devices ports...\n")

        if os.name == 'nt':
            for i in range(numof_ports_searched):  # Iterates through ports on computer
                portString = "COM " + str(i)
                try:
                    # baud rate set for device
                    gps = GPS(port=portString, baud_rate=9600)
                    print("Device found on port " + str(i) + "!")
                    return gps
                except:
                    if i == (numof_ports_searched-1):
                        print("Warning: No GPS device found on your system!")
                        print(
                            "The system will be unable to extract coordinates upon detection!\n")
        if os.name == 'posix':
            try:
                portString = "/dev/tty.usbmodem143301"
                # baud rate set for device
                gps = GPS(port=portString, baud_rate=9600)
                print("Device found on port!")
                return gps
            except:
                print("Warning: No GPS device found on your system!")
                print(
                    "The system will be unable to extract coordinates upon detection!\n")
        return gps  # if there is no gps self.gps will be None

    def toggle_device(self):
        if self.gps is not None:
            self.gps = None
            print("Turning off Device")
        elif self.gps is None:
            self.gps = self.get_gps_device()
    # get gps status

    def get_gps_status(self):
        if self.gps:
            return self.gps
        else:
            return None

    def convert_gpgga_to_lat_long(self, raw_data):
        """I chose to do this over simply getting the lat long from the gps because it would mislabel the long to be east (positve value)
        this would result in the map loading a remote location in Western China. This corrects the orientation everytime   """
        try:
            lat_deg = int(raw_data[2][:2])
            lat_min = float(raw_data[2][2:])
            lat = lat_deg + (lat_min / 60)

            if raw_data[3] == "S":
                lat = -lat

            long_deg = int(raw_data[4][:3])
            long_min = float(raw_data[4][3:])
            long = long_deg + (long_min / 60)

            if raw_data[5] == "W":
                long = -long

            return lat, long
        except:
            print(
                "Unknown error while transforming coordinates -- Returning coordinates [0,0]")
            return "0,0"

    def extract_coordinates(self):
        if self.gps is None:
            # print('GPS IS OFF OR NOT PLUGGED IN')
            self.last_coords = "0,0"
            return self.last_coords

        try:
            raw_data = self.gps.get_raw_data()
            coord = self.convert_gpgga_to_lat_long(raw_data)
            coord = str(coord).replace("(", "").replace(")", "")
            self.last_coords = str(coord)
            print("extract_coordinates: " + coord)
            return self.last_coords
        except:
            return "0,0"


# Test case (only executes when this script is run directly, not when imported)
if __name__ == "__main__":
    gp = GPS_Controller()
    # print(gp.gps.get_lat_long())

    raw_data = gp.gps.get_raw_data()
    print(raw_data)
    coords = gp.convert_gpgga_to_lat_long(raw_data)
    print(coords)
    coord = str(coords).replace("(", "").replace(")", "")
    print(coord)

    gp.toggle_device()
    print(gp.get_gps_status())
    gs = GPS_Controller()
    raw_dat = gs.gps.get_raw_data()
    conv = gs.convert_gpgga_to_lat_long(raw_dat)
    print(conv)
    # m = folium.Map(location=coords, zoom_start=20)

    # tile = folium.TileLayer(
    #     tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    #     attr='Esri',
    #     name='Esri Satellite',
    #     overlay=False,
    #     control=True
    # ).add_to(m)
    # m.save("map.html")

    # ser = serial.Serial('/dev/tty.usbmodem143301', 9600, timeout=1)
    # def readgps():
    #     """Read the GPG LINE using the NMEA standard"""
    #     while True:
    #         line = ser.readline()
    #         if "GPGGA" in line:
    #             # Yes it is positional info for lattitude
    #             latitude = line[18:26]
    #             longitude = line[31:39]  # do it again
    #             print(latitude, longitude)
    #             return (latitude, longitude)
    # readgps()
