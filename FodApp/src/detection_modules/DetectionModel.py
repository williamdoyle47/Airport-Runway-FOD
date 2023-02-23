import tensorflow as tf
import os
import cv2
import json
import random
import requests
import uuid
import numpy as np
from detection_modules.DetectionLogging import LogDetection
from PIL import Image
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from detection_modules.coords import *
from object_detection.builders import model_builder
from object_detection.utils import config_util
import requests
from detection_modules.coords import coords, magnet, sweeping, rumble_strips, fod_containers
from detection_modules.tracker import *

camera_Width = 480  # 320 # 480 # 720 # 1080 # 1620
camera_Height = 360  # 240 # 360 # 540 # 810  # 1215
frameSize = (camera_Width, camera_Height)


class DetectionModel:
    def __init__(self):
        self.pathnumber = 1
        self.label_id_offset = 1
        self.threshold = .70
        self.url = "http://127.0.0.1:8000/add_fod"
        self.saved_model_path = "/Users/williamdoyle/Documents/GitHub/Airport-Runway-FOD/FodApp/src/Tensorflow/workspace/models/ssd_mobnet640v2/export/saved_model"
        self.label_map_name = "/Users/williamdoyle/Documents/GitHub/Airport-Runway-FOD/FodApp/src/Tensorflow/workspace/annotations/label_map.pbtxt"
        self.tracker = EuclideanDistTracker()
        self.load_model()

    def load_model(self):
        try:
            self.saved_model = tf.saved_model.load(self.saved_model_path)

            self.category_index = label_map_util.create_category_index_from_labelmap(
                self.label_map_name)
        except:
            print("Error loading model -- check saved model")

    @tf.function  # graph mode execution decorator -- pre loads model weights leading to faster inference
    # Connect to tf obj detection api to make detection using our model
    def detect_fn(self, input_tensor):
        detections = self.saved_model(input_tensor)
        return detections

    def make_detections(self, image_np):

        # Pre Process Image Frame
        input_tensor = tf.convert_to_tensor(image_np)
        input_tensor = input_tensor[tf.newaxis, ...]
        input_tensor = input_tensor[:, :, :, :3]

        # manipulate prediction dict
        detections = self.detect_fn(input_tensor)
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                      for key, value in detections.items()}
        detections['num_detections'] = num_detections
        detections['detection_classes'] = detections['detection_classes'].astype(
            np.int64)

        return detections

    # old bnd box

    def bndbox(self, image_np, detections):

        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np,
            detections['detection_boxes'],
            detections['detection_classes'] + self.label_id_offset,
            detections['detection_scores'],
            self.category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=5,
            min_score_thresh=.6,
            agnostic_mode=False)
        return image_np

    def findScore(self, scoreValues):  # finds the score of each detection
        found = [i for i, e in enumerate(scoreValues) if e >= self.threshold]
        return found

    def detection_controller(self, image_np):
        try:
            listDetections = []  # for tracker
            detections = self.make_detections(
                image_np)  # get detections from frame

            # Gets the detection coordinates from the detections object and adds to array for tracking
            positionList = self.findScore(
                detections['detection_scores'])  # return
            for position in positionList:
                # detect --> [ymin, xmin, ymax, xmax]
                detect = detections['detection_boxes'][position]
                x, y, w, h = (
                    detect[1] * camera_Width, detect[0] * camera_Height, detect[3] * camera_Width, detect[2] * camera_Height)
                listDetections.append([x, y, w, h])

            frame = cv.resize(image_np, frameSize)

            # Object tracking and Detection Logging
            boxes_ids = self.tracker.update(
                listDetections, self.category_index, detections, frame)

            # Add bnd boxes to detected object -- detection classes + id
            for box_id in boxes_ids:
                x, y, w, h, id = box_id
                cv.putText(frame, self.category_index.get(
                    (detections['detection_classes'][0] + self.label_id_offset))['name'] + " " + str(id), (int(x), int(y) - 15),
                    cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                cv.rectangle(frame, (int(x), int(y)),
                             (int(w), int(h)), (0, 255, 0), 3)

            return frame  # return frame
        except:
            return image_np  # return frmae even when no object detected


# FOR TESTING
if __name__ == '__main__':
    print(os.getcwd())
    cap = cv2.VideoCapture(1)
    det = DetectionModel()
    while (cap.isOpened()):

        ret, frame = cap.read()
        #cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

        if ret:
            image_np = np.array(frame)
            frame = det.detection_controller(image_np)
            cv2.imshow("Image", frame)
        else:
            print('no video')
            continue

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# some code borrowed from places such as stackoverflow.com
# and https://www.youtube.com/watch?v=yqkISICHH-U&t=11619s
