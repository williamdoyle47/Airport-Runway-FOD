import time
import operator
import PySimpleGUI as sg
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os
import playsound
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util

threshold = .4

CUSTOM_MODEL_NAME = 'my_efficentdet_d2_GLTandFirstGoProImages-50k'
PRETRAINED_MODEL_NAME = 'efficentDet2-FGPandGLT-50k-04.tar.gz'
PRETRAINED_MODEL_URL = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz'
TF_RECORD_SCRIPT_NAME = 'generate_tfrecord.py'
LABEL_MAP_NAME = 'label_map.pbtxt'
#detect_fn = tf.saved_model.load("Tensorflow\workspace\pre-trained-models\ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8\saved_model")

#Efficent det2 path
d2PathCkpt = 'Tensorflow/workspace/models/my_efficentdet_d2_GLTandFirstGoProImages-50k'
d2Config = 'Tensorflow/workspace/models/my_efficentdet_d2_GLTandFirstGoProImages-50k/pipeline.config'

# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(d2Config)
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(d2PathCkpt, 'ckpt-51')).expect_partial()

paths = {
    "WORKSPACE_PATH": os.path.join("Tensorflow", "workspace"),
    "SCRIPTS_PATH": os.path.join("Tensorflow", "scripts"),
    "APIMODEL_PATH": os.path.join("Tensorflow", "models"),
    "ANNOTATION_PATH": os.path.join("Tensorflow", "workspace", "annotations"),
    "IMAGE_PATH": os.path.join("Tensorflow", "workspace", "images"),
    "MODEL_PATH": os.path.join("Tensorflow", "workspace", "models"),
    "PRETRAINED_MODEL_PATH": os.path.join(
        "Tensorflow", "workspace", "pre-trained-models"
    ),
    "CHECKPOINT_PATH": os.path.join(
        "Tensorflow", "workspace", "models", CUSTOM_MODEL_NAME
    ),
    "OUTPUT_PATH": os.path.join(
        "Tensorflow", "workspace", "models", CUSTOM_MODEL_NAME, "export"
    ),
    "TFJS_PATH": os.path.join(
        "Tensorflow", "workspace", "models", CUSTOM_MODEL_NAME, "tfjsexport"
    ),
    "TFLITE_PATH": os.path.join(
        "Tensorflow", "workspace", "models", CUSTOM_MODEL_NAME, "tfliteexport"
    ),
    "PROTOC_PATH": os.path.join("Tensorflow", "protoc"),
}

files = {
    "PIPELINE_CONFIG": os.path.join(
        "Tensorflow", "workspace", "models", CUSTOM_MODEL_NAME, "pipeline.config"
    ),
    "TF_RECORD_SCRIPT": os.path.join(paths["SCRIPTS_PATH"], TF_RECORD_SCRIPT_NAME),
    "LABELMAP": os.path.join(paths["ANNOTATION_PATH"], LABEL_MAP_NAME),
}

category_index = label_map_util.create_category_index_from_labelmap(files['LABELMAP'])
# Camera Settings
camera_Width  = 480 # 320 # 480 # 720 # 1080 # 1620
camera_Heigth = 360 # 240 # 360 # 540 # 810  # 1215
frameSize = (camera_Width, camera_Heigth)
video_capture1 = cv.VideoCapture(0)
video_capture2 = cv.VideoCapture(1)
video_capture3 = cv.VideoCapture(2)
video_capture4 = cv.VideoCapture(3)
video_capture5 = cv.VideoCapture(4)
time.sleep(2.0)

# init Windows Manager
sg.theme("Black")

# def webcam col
cameracolumn_layout = [[sg.Text("Choose how many camera's you want to display", size=(60,1))], [sg.Combo(["1", "2", "3", "4", "5"], key="cameraAmount", default_value="5")]]

cameracolumn = sg.Column(cameracolumn_layout, element_justification='center', background_color="black")

threshcolumn_layout = [[sg.Text("Choose the threshold you want to use", size=(60,1))], [sg.Combo(["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"], key="threshAmount", default_value=str(int(threshold*100))+'%')]]

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

colslayout = [[cameracolumn, threshcolumn], [colwebcam1, colwebcam2], [colwebcam3, colwebcam4], [colwebcam5, coltextbox]]

layout = [colslayout]

window    = sg.Window("FOD Detection", layout,
                    no_titlebar=False, alpha_channel=1, grab_anywhere=False,
                    return_keyboard_events=True, location=(100, 100))


@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections

def findScore(scoreValues):
    found = []
    found = [i for i, e in enumerate(scoreValues) if e >= threshold]
    return found

def tfBoundingBoxes(frame, detectionKey, detectionKey2):
    image_np = np.array(frame)
    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
    detections = detect_fn(input_tensor)
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                  for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    label_id_offset = 1
    image_np_with_detections = image_np.copy()

    viz_utils.visualize_boxes_and_labels_on_image_array(
                image_np_with_detections,
                detections['detection_boxes'],
                detections['detection_classes']+label_id_offset,
                detections['detection_scores'],
                category_index,
                use_normalized_coordinates=True,
                max_boxes_to_draw=5,
                min_score_thresh=threshold,
                agnostic_mode=False)

    frame = cv.resize(image_np_with_detections, frameSize)

    positionList = findScore(detections['detection_scores'])
    #print(str(positionList) + "list")
    
    if positionList != []:        
        window[detectionKey].Widget.config(background='red')
        window[detectionKey2].Widget.config(background='red')
        #playsound._playsoundWin('alarm.wav')

        #display to textbox
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

while True:
    start_time = time.time()
    event, values = window.read(timeout=20)

    if event == sg.WIN_CLOSED:
        break

    ret, frame1 = video_capture1.read()
    #ret, frame2 = video_capture2.read()
    #ret, frame3 = video_capture3.read()
    #ret, frame4 = video_capture4.read()
    #ret, frame5 = video_capture5.read()

    tfBoundingBoxes(frame1, "cam1", "cam1Update")
    #tfBoundingBoxes(frame2, "cam2", "cam2Update")
    #tfBoundingBoxes(frame3, "cam3", "cam3Update")
    #tfBoundingBoxes(frame4, "cam4", "cam4Update")
    #tfBoundingBoxes(frame5, "cam5", "cam5Update")
        

video_capture1.release()
video_capture2.release()
video_capture3.release()
video_capture4.release()
video_capture5.release()
cv.destroyAllWindows()