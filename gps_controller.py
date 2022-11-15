# This script is used for extracting the coordinates from the raw data of the GPS puck.
from logging import exception
from pyembedded.gps_module.gps import GPS
import os 

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
        

        if os.name=='nt':
            for i in range(numof_ports_searched): #Iterates through ports on computer 
                portString = "COM " + str(i)
                try:
                    gps = GPS(port=portString, baud_rate=9600) #baud rate set for device
                    print("Device found on port " + str(i) + "!")
                    return gps
                except: 
                    if i == (numof_ports_searched-1):
                        print("Warning: No GPS device found on your system!")
                        print("The system will be unable to extract coordinates upon detection!\n")
        if os.name=='posix':
                try:
                    portString = "/dev/tty.usbmodem143201"
                    gps = GPS(port=portString, baud_rate=9600) #baud rate set for device
                    print("Device found on port!")
                    return gps
                except: 
                        print("Warning: No GPS device found on your system!")
                        print("The system will be unable to extract coordinates upon detection!\n")
        return gps #if there is no gps self.gps will be None

    def toggle_device(self):
        if self.gps is not None:
            self.gps = None
            print("Device Turned off")
        elif self.gps is None:
            self.gps = self.get_gps_device()
    #get gps status
    def get_gps_status(self):
        if self.gps is None:
            return None
        return self.gps
    # The following function takes raw data (array) as argument, returns [longitude, latitude] as decimal degrees.
    # Raw data is in NMEA format, so we need to parse the numbers to get the true decimal-degree coordinates.
    # For example, 09349.7112 West is actually -93.82852 because the first digits (093) indicate degrees, 
    # while the rest of the number (49.7...) indicates the minutes.
    # West and South correspond to negative values for latitude and longitude, respectively.
    def transform_coordinates(self, raw_data):
        try:
            lati = raw_data[0]
            longi = raw_data[1]
            if isinstance(lati, str):
                lati = 0
            if isinstance(longi, str):
                longi = 0
            negative_check = self.gps.get_raw_data()
            if negative_check[3] == 'S':
                lati *= -1
            if negative_check[5] == 'W':
                longi *= -1

            # Returning the latitude and longitude to be used for placing point on map
            return [lati, longi]
        except:
            print("Unknown error while transforming coordinates -- Returning coordinates [0,0]")
            return [0,0]


    def get_raw_gps(self): # Returns raw data from GPS as an array
        try:
            # Raw GPS data extracted from GPS device via the gps object
            coords = self.gps.get_lat_long() 
            raw_data = list(coords)
            # print(raw_data)
            return raw_data
        except: 
            print("Unable to get raw data")
            return [0,0]

    def extract_coordinates(self):
        if self.gps is None:
            # print('GPS IS OFF OR NOT PLUGGED IN')
            self.last_coords = [0,0]
            return self.last_coords

        try:
            raw_data = self.get_raw_gps()
            transformed = self.transform_coordinates(raw_data)
            self.last_coords = transformed
            print("extract_coordinates: " + str(transformed))
            return self.last_coords
        except:
            return [0, 0]

# Test case (only executes when this script is run directly, not when imported)
if __name__ == "__main__":

    gps_controller = GPS_Controller()
    raw_data = gps_controller.get_raw_gps()
    print(raw_data)

    transformed = gps_controller.transform_coordinates(raw_data)
    print(transformed)

    blank = list()
    blank.append('N/A')
    blank.append('N/A')
    testblank = gps_controller.transform_coordinates(blank)
    print(testblank)

    extracted = gps_controller.extract_coordinates()
    print(extracted)