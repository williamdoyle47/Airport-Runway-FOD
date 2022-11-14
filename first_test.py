import time
import PySimpleGUI as sg
from utility.detected_image_folder_funcs import *
from utility.map_utils import *
from gps_controller import *
from threading import Thread
from tracker import *
from gui_comp import *
from data_model_interactions import *
from utility.gui_utils import *
from main import *

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