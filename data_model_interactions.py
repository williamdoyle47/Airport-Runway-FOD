import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
from utility.detected_image_folder_funcs import * 
from utility.map_utils import *

# Label map path
LABEL_MAP_NAME = 'Tensorflow/workspace/annotations/label_map.pbtxt'
#Model path
d2PathCkpt = 'Tensorflow/workspace/models/my_ssd_mobnet'
d2Config = 'Tensorflow/workspace/models/my_ssd_mobnet/pipeline.config'
# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(d2Config)
detection_model = model_builder.build(model_config=configs['model'], is_training=False)
# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(d2PathCkpt, 'ckpt-3')).expect_partial() #ensure up to date with current checkpoint
category_index = label_map_util.create_category_index_from_labelmap(LABEL_MAP_NAME)

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections

def findScore(scoreValues, threshold): # finds the score of each detection
    found = [i for i, e in enumerate(scoreValues) if e >= threshold]
    return found

def tfBoundingBoxes(frame, detectionKey, detectionKey2, threshold, frameSize, tracker, gps_controller, mapping, window):
    image_np = np.array(frame)
    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
    detections = detect_fn(input_tensor)
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                  for key, value in detections.items()}
    
    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    # Used for object tracking
    listDetections = []

    #List of objects position in detections[] with a certain threshold
    positionList = findScore(detections['detection_scores'], threshold)

    # Gets the detection coordinates from the detections object and adds to array for tracking
    for position in positionList:
        # detect --> [ymin, xmin, ymax, xmax]
        camera_Width, camera_Height = frameSize
        detect = detections['detection_boxes'][position]
        x, y, w, h = (
        detect[1] * camera_Width, detect[0] * camera_Height, detect[3] * camera_Width, detect[2] * camera_Height)
        listDetections.append([x, y, w, h])

    frame = cv.resize(image_np, frameSize)

    # Object Tracking
    boxes_ids = tracker.update(listDetections, frame, gps_controller, mapping)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv.putText(frame, str(id), (int(x), int(y) - 15), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv.rectangle(frame, (int(x), int(y)), (int(w), int(h)), (0, 255, 0), 3)

    if positionList != []: #if position list is not empty means there is a detection
        window[detectionKey].Widget.config(background='red')
        window[detectionKey2].Widget.config(background='red')
        # playsound._playsoundWin('alarm.wav')
        ### Moved - tracker.py calls det to write to log
        # display to textbox
        # for position in positionList:
        #     if (
        #     category_index.get(detections['detection_classes'][position] == detections['detection_classes'][position])):
        #         # print(str(category_index.get(detections['detection_classes'][position]+1)) + " on " + detectionKey)
        #         window["textbox"].update(window["textbox"].get() + "\n" + str(
        #             category_index.get(detections['detection_classes'][position] + 1)) + " on " + detectionKey)
        #         with open("Log.txt", "wt") as text_file:
        #             text_file.write(str(window["textbox"].get()))

        # print(str(detections['detection_classes']) + "was found on " + detectionKey)
    else:
        window[detectionKey].Widget.config(background='black')
        window[detectionKey2].Widget.config(background='black')

    # Update camera
    imgbytes = cv.imencode(".png", frame)[1].tobytes()
    window[detectionKey].update(data=imgbytes)