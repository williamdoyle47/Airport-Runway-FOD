from gps_controller import *

#def constants():

def test_disconnect_gps():
     gps_controller = GPS_Controller()
     gps_controller.toggle_device()
     assert gps_controller.gps is None

def test_connect_gps():
     gps_controller = GPS_Controller()
     assert gps_controller.gps is not None

def test_reconnect_gps():
     gps_controller = GPS_Controller()
     gps_controller.toggle_device()
     gps_controller.toggle_device()
     assert gps_controller.gps is None