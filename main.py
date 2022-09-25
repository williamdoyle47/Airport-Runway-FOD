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

def main():
    # Create folder for storing snapshots of detections (if not already created)
    create_folder("detectionImages")
    # Clear detections from past runs
    delete_folder_contents("detectionImages")
    #Clear log file
    clearLog()

    window = sg.Window("FOD Detection", layout,
                        no_titlebar=False, alpha_channel=1, grab_anywhere=False,
                        return_keyboard_events=True, location=(100, 100)).Finalize()

    # Initialize GPS controller
    gps_controller = GPS_Controller() #Returns None if no gps device

    #Initialize object tracking object
    tracker = EuclideanDistTracker()

    # Initialize coordinates
    try: # if gps is accessible
        starting_coords = gps_controller.extract_coordinates()
    except: # if unable to access gps
        starting_coords = [0,0]
        print("unable to get starting coordinates - defaulting to 0,0")

    # Initialize map
    mapping = createMap(starting_coords)

    # Spawn thread for concurrent GPS reading (to bypass Input/Output delay of live reads)
    thread = Thread(target=gps_controller.extract_coordinates)
    thread.start()

    while True:
        start_time = time.time()
        event, values = window.read(timeout=20)

        if not thread.is_alive():
            # print("thread completed")
            thread = Thread(target=gps_controller.extract_coordinates)
            thread.start()

        if event == sg.WIN_CLOSED:
            break
        if event == 'Map':
            openMap(tracker)
        if event == 'GPS':
            gps_controller.toggle_device()
        

        threshold = getThreshold(values['threshAmount'])
        cameraAmount = getCameraAmount(values['cameraAmount'])
        selectCamera(cameraAmount, values, threshold, tracker, gps_controller, mapping, window)

    # Upon exit, destroys all cameras and windows
    destory_camera_windows()

if __name__ == '__main__':
    main()
