import time
import operator
import PySimpleGUI as sg
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os
import playsound
import tensorflow as tf
import folium
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import base64
import webbrowser
import folium
from folium import IFrame
from Detection import Detection
import os, shutil
from tracker import *
from extract_coordinates import *
from threading import Thread



def create_folder(folderName):
    exists = os.path.exists(folderName)
    if not exists:
        os.makedirs(folderName)

def delete_folder_contents(folderPath):
    for filename in os.listdir(folderPath):
        file_path = os.path.join(folderPath, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    print("Contents of folder deleted: " + folderPath)

def createMap():
    # map initializer
    map = folium.Map(location=[45.550120, -94.152411], zoom_start=20)

    tile = folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri Satellite',
        overlay=False,
        control=True
    ).add_to(map)

    return map

def openMap():
    webbrowser.open("map.html")

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections

def findScore(scoreValues, threshold):
    found = [i for i, e in enumerate(scoreValues) if e >= threshold]
    return found

def setThreshold(threshString):
    threshold = int(threshString[:-1])
    return threshold / 100

def getCameraAmount(cameraString):
    amount = int(cameraString)
    return amount

def newDetection():
    #playsound._playsoundWin('alarm.wav')
    # det object
    det = Detection("placeholderType", map)
    # Save detection as image done in the tracker.py file
    detList.append(det)

def getCameraChoice(choice):
    choiceInt = int(choice)
    if choiceInt == 1:
       frame = video_capture1.read()
    elif choiceInt == 2:
       frame = video_capture2.read()
    elif choiceInt == 3:
       frame = video_capture3.read()
    elif choiceInt == 4:
       frame = video_capture4.read()
    elif choiceInt == 5:
       frame = video_capture5.read()
    return frame

# Create folder for storing snapshots of detections (if not already created)
create_folder("detectionImages")

# Clear detections from past runs
delete_folder_contents("detectionImages")

# Create tracker object
tracker = EuclideanDistTracker()

LABEL_MAP_NAME = 'label_map.pbtxt'
#detect_fn = tf.saved_model.load("Tensorflow\workspace\pre-trained-models\ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8\saved_model")

#Model config pathes path
d2PathCkpt = 'Tensorflow/workspace/models/my_ssd_mobnet'
d2Config = 'Tensorflow/workspace/models/my_ssd_mobnet/pipeline.config'

# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(d2Config)
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(d2PathCkpt, 'ckpt-51')).expect_partial()

category_index = label_map_util.create_category_index_from_labelmap(LABEL_MAP_NAME)
# Camera Settings
camera_Width  = 480 # 320 # 480 # 720 # 1080 # 1620
camera_Height = 360 # 240 # 360 # 540 # 810  # 1215
frameSize = (camera_Width, camera_Height)
video_capture1 = cv.VideoCapture('Video 2.mp4')
video_capture2 = cv.VideoCapture(1)
video_capture3 = cv.VideoCapture(2)
video_capture4 = cv.VideoCapture(3)
video_capture5 = cv.VideoCapture(4)
time.sleep(2.0)

# init Windows Manager
sg.theme("Black")

# def webcam col
cameracolumn_layout = [[sg.Text("Choose how many camera's you want to display", size=(60,1))], [sg.Combo(["1", "2", "3", "4", "5"], key="cameraAmount", default_value="1")]]

cameracolumn = sg.Column(cameracolumn_layout, element_justification='center', background_color="black")

mapbutton_layout = [[sg.Text("Open Map", size=(60,1), justification='center')], [sg.Button('Map')]]

mapbutton = sg.Column(mapbutton_layout, element_justification='center', background_color="black")

blankcolumn_layout = [[sg.Text("", size=(60,1))], [sg.Text("")]]

blankcolumn = sg.Column(blankcolumn_layout, element_justification='center', background_color="black")

threshcolumn_layout = [[sg.Text("Choose the threshold you want to use", size=(60,1))], [sg.Combo(["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"], key='threshAmount', default_value="60%")]]

threshcolumn = sg.Column(threshcolumn_layout, element_justification='center', background_color="black")

colwebcam1_layout = [[sg.Text("Camera 1 (Front Driver)", size=(60, 1), background_color='black', justification="center")],
                        [sg.Image(filename="", key="cam1")]]
colwebcam1 = sg.Column(colwebcam1_layout, element_justification='center', key="cam1Update", background_color='black')

colwebcam2_layout = [[sg.Text("Camera 2 (Front Passenger)", size=(60, 1), justification="center")],
                        [sg.Image(filename="", key="cam2")]]
colwebcam2 = sg.Column(colwebcam2_layout, element_justification='center', key="cam2Update", background_color='black')

colwebcam3_layout = [[sg.Text("Camera 3 (Driver Side)", size=(60, 1), justification="center")],
                        [sg.Image(filename="", key="cam3")]]
colwebcam3 = sg.Column(colwebcam3_layout, element_justification='center', key="cam3Update", background_color='black')

colwebcam4_layout = [[sg.Text("Camera 4 (Passenger Side)", size=(60, 1), justification="center")],
                        [sg.Image(filename="", key="cam4")]]
colwebcam4 = sg.Column(colwebcam4_layout, element_justification='center', key="cam4Update", background_color='black')

colwebcam5_layout = [[sg.Text("Camera 5 (Rear)", size=(60, 1), justification="center")],
                        [sg.Image(filename="", key="cam5")]]
colwebcam5 = sg.Column(colwebcam5_layout, element_justification='center', key="cam5Update", background_color='black')

coltextbox_layout = [[sg.Text("Output", size=(60,1), justification="center")],
                        [sg.Multiline(size=(60, 30), key="textbox", autoscroll=True, disabled=True)]]
coltextbox = sg.Column(coltextbox_layout, element_justification='center')

colslayout = [[cameracolumn, mapbutton, threshcolumn], [colwebcam1, colwebcam2, colwebcam3], [colwebcam4, colwebcam5, coltextbox]]

layout = [colslayout]

window    = sg.Window("FOD Detection", layout,
                    no_titlebar=False, alpha_channel=1, grab_anywhere=False,
                    return_keyboard_events=True, location=(100, 100)).Finalize()

# Initialize GPS controller
gps_controller = GPS_Controller()
gps_controller = None

print("Line 189")

try: # if gps is accessible
    print("Line 192")
    starting_coords = gps_controller.extract_coordinates()
    print("Line 194")
except: # if unable to access gps
    print("Line 196")
    createMap()

print("Line 199")
def openMap(m, detections_list):

    for det in detections_list:
        det.addPoint()

    webbrowser.open("map.html")

def tfBoundingBoxes(frame, detectionKey, detectionKey2, threshold, detections_list):
    image_np = np.array(frame)
    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
    detections = detect_fn(input_tensor)
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                  for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    #Used for object tracking
    listDetections = []

    #List of the objects position in array above certain threshold
    positionList = findScore(detections['detection_scores'], threshold)

    # Gets the detection coordinates from the detections object and adds to array for tracking
    for position in positionList:
        # detect --> [ymin, xmin, ymax, xmax]
        detect = detections['detection_boxes'][position]
        x, y, w, h = (detect[1] * camera_Width, detect[0] * camera_Height, detect[3] * camera_Width, detect[2] * camera_Height)
        listDetections.append([x, y, w, h])

    frame = cv.resize(image_np, frameSize)

    # det object to take image of if it is a new object
    det = Detection(map)

    # Object Tracking
    boxes_ids = tracker.update(listDetections, frame, det)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv.putText(frame, str(id), (int(x), int(y) - 15), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv.rectangle(frame, (int(x), int(y)), (int(w), int(h)), (0, 255, 0), 3)

    if positionList != []:        
        window[detectionKey].Widget.config(background='red')
        window[detectionKey2].Widget.config(background='red')

        #display to textbox
        # ToDo: Move this to a function to print to log only once? Is it necessary to keep this if we are using 'Object' as label?
        for position in positionList:
            if(category_index.get(detections['detection_classes'][position] == detections['detection_classes'][position])):
                #print(str(category_index.get(detections['detection_classes'][position]+1)) + " on " + detectionKey)
                window["textbox"].update(window["textbox"].get() + "\n" + str(category_index.get(detections['detection_classes'][position]+1)) + " on " + detectionKey)
                with open("Log.txt", "wt") as text_file:
                    text_file.write(str(window["textbox"].get()))

        #print(str(detections['detection_classes']) + "was found on " + detectionKey)
    else:
        window[detectionKey].Widget.config(background='black')
        window[detectionKey2].Widget.config(background='black')

    #Update camera
    imgbytes = cv.imencode(".png", frame)[1].tobytes()
    window[detectionKey].update(data=imgbytes)
    
thread = Thread(target=gps_controller.extract_coordinates)
thread.start()

detections_list = []

# Spawn thread for concurrent GPS reading (to bypass Input/Output delay of live reads)

thread = Thread(target=gps_controller.extract_coordinates)
thread.start()

while True:
    start_time = time.time()
    event, values = window.read(timeout=20)

    if thread.is_alive() == False:
        print("thread completed")
        thread = Thread(target=gps_controller.extract_coordinates)
        thread.start()

    if event == sg.WIN_CLOSED:
        break
    if event == 'Map':
        openMap(m, detections_list)

    if (cameraAmount == 1):
        ret, frame1 = getCameraChoice(values['choice1'])
        tfBoundingBoxes(frame1, "cam1", "cam1Update", threshold)
    elif (cameraAmount == 2):
        ret, frame1 = getCameraChoice(values['choice1'])
        tfBoundingBoxes(frame1, "cam1", "cam1Update", threshold)
        ret, frame2 = getCameraChoice(values['choice2'])
        tfBoundingBoxes(frame2, "cam2", "cam2Update", threshold)
    elif (cameraAmount == 3):
        ret, frame1 = getCameraChoice(values['choice1'])
        tfBoundingBoxes(frame1, "cam1", "cam1Update", threshold)
        ret, frame2 = getCameraChoice(values['choice2'])
        tfBoundingBoxes(frame2, "cam2", "cam2Update", threshold)
        ret, frame3 = getCameraChoice(values['choice3'])
        tfBoundingBoxes(frame3, "cam3", "cam3Update", threshold)
    elif (cameraAmount == 4):
        ret, frame1 = getCameraChoice(values['choice1'])
        tfBoundingBoxes(frame1, "cam1", "cam1Update", threshold)
        ret, frame2 = getCameraChoice(values['choice2'])
        tfBoundingBoxes(frame2, "cam2", "cam2Update", threshold)
        ret, frame3 = getCameraChoice(values['choice3'])
        tfBoundingBoxes(frame3, "cam3", "cam3Update", threshold)
        ret, frame4 = getCameraChoice(values['choice4'])
        tfBoundingBoxes(frame4, "cam4", "cam4Update", threshold)
    elif (cameraAmount == 5):
        ret, frame1 = getCameraChoice(values['choice1'])
        tfBoundingBoxes(frame1, "cam1", "cam1Update", threshold)
        ret, frame2 = getCameraChoice(values['choice2'])
        tfBoundingBoxes(frame2, "cam2", "cam2Update", threshold)
        ret, frame3 = getCameraChoice(values['choice3'])
        tfBoundingBoxes(frame3, "cam3", "cam3Update", threshold)
        ret, frame4 = getCameraChoice(values['choice4'])
        tfBoundingBoxes(frame4, "cam4", "cam4Update", threshold)
        ret, frame5 = getCameraChoice(values['choice5'])
        tfBoundingBoxes(frame5, "cam5", "cam5Update", threshold)
        

video_capture1.release()
video_capture2.release()
video_capture3.release()
video_capture4.release()
video_capture5.release()
cv.destroyAllWindows()