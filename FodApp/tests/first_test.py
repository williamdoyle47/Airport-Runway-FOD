import time
import PySimpleGUI as sg
from utility.detected_image_folder_funcs import *
from utility.map_utils import *
from FodApp.gps_controller import *
from threading import Thread
from FodApp.tracker import *
from Archive.old_code.gui_comp import *
from Archive.old_code.data_model_interactions import *
from utility.gui_utils import *
from Archive.old_code.main import *

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