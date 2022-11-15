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

#def constants():

#emulates setting up and closing the main to test and measure how long such an action would take and test if the main still opens
def test_main():
    create_folder("detectionImages")
    delete_folder_contents("detectionImages")
    clearLog()
    window = sg.Window("FOD Detection", layout,
                       no_titlebar=False, alpha_channel=1, grab_anywhere=False,
                       return_keyboard_events=True, location=(100, 100)).Finalize()
    gps_controller = GPS_Controller()
    tracker = EuclideanDistTracker()
    try:
        starting_coords = gps_controller.extract_coordinates()
    except:
        starting_coords = [0, 0]
        print("unable to get starting coordinates - defaulting to 0,0")
    mapping = createMap(starting_coords)
    thread = Thread(target=gps_controller.extract_coordinates)
    thread.start()
    while True:
        start_time = time.time()
        event, values = window.read(timeout=20)
        if not thread.is_alive():
            thread = Thread(target=gps_controller.extract_coordinates)
            thread.start()
        break
    destory_camera_windows()