from gps_controller import *

#def constants():

def test_null_coords():
    gps_controller = GPS_Controller()
    blank = list()
    blank.append('N/A')
    blank.append('N/A')
    testblank = gps_controller.transform_coordinates(blank)
    print(testblank)

def test_connected_coords():
    gps_controller = GPS_Controller()
    extracted = gps_controller.extract_coordinates()
    print(extracted)

def test_transformed_coords():
    gps_controller = GPS_Controller()
    raw_data = gps_controller.get_raw_gps()
    transformed = gps_controller.transform_coordinates(raw_data)
    print(transformed)