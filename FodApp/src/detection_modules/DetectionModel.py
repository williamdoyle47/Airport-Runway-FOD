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


class DetectionModel:
    def __init__(self):
        self.pathnumber = 1
        self.label_id_offset = 1
        self.threshold = .70
        self.url = "http://127.0.0.1:8000/add_fod"
        self.saved_model_path = "/Users/User/Documents/GitHub/Airport-Runway-FOD/FodApp/src/Tensorflow/workspace/workspace/models/ssd_mobnet640/export/saved_model"
        self.label_map_name = "/Users/User/Documents/GitHub/Airport-Runway-FOD/FodApp/src/Tensorflow/workspace/annotations/label_map.pbtxt"
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

    # def bndcoords(self, image_np, detections):  # Crop image
    #     im = Image.fromarray(image_np)
    #     im_width = im.width
    #     im_height = im.height
    #     xmin, ymin, xmax, ymax = detections['detection_boxes'][0]
    #     (x, x2, y, y2) = (xmin * im_width, xmax *
    #                       im_width, ymin * im_height, ymax * im_height)
    #     w = x2-x
    #     h = y2-y
    #     return x, y, w, h

    def recommend_action(self, fod_type):
        if fod_type in magnet:
            rec_cleanup_method = 'magnet'
        elif fod_type in sweeping:
            rec_cleanup_method = 'sweeping'
        elif fod_type in fod_containers:
            rec_cleanup_method = 'fod_containers'
        elif fod_type in rumble_strips:
            rec_cleanup_method = 'rumble_strips'
        else:
            rec_cleanup_method = 'Not sure'
        return rec_cleanup_method

    def logging_detection(self, detections, boundary_boxes):

        confidence_score = detections['detection_scores'][0]
        fod_uuid = uuid.uuid4()

        # store images by uuid
        try:
            magnet = ['metal', 'screw']  # metallic objects
            sweeping = ['pen', 'glove', 'cloth', 'LuggageTag']
            rumble_strips = ['']
            fod_containers = ['wood']

            fod_type = self.category_index.get(
                (detections['detection_classes'][0] + self.label_id_offset))['name']  # get deteection class
            image_path = "/Users/User/Documents/GitHub/Airport-Runway-FOD/FodApp/src/data_modules/detectionImages/" + \
                str(fod_uuid) + '.jpg'
            cropped = Image.fromarray(boundary_boxes)
            cropped.save(image_path, 'JPEG')
        except:
            print("exception occured in logging detection")
            return

        # Log detected fod to database using post request
        rec_cleanup_method = self.recommend_action(fod_type)
        cleaned = False
        coor = random.choice(coords)

        image_path = "/detectionImages/" + str(fod_uuid) + '.jpg'  # fix this
        image_path = "../../data_modules/detectionImages/" + \
            str(self.pathnumber) + '.jpg'

        det_json_obj = {'fod_type': str(fod_type),
                        'uuid': str(fod_uuid),
                        'coord': str(coor),
                        'confidence_level': float(confidence_score),
                        'image_path': str(image_path),
                        'cleaned': bool(cleaned),
                        'recommended_action': str(rec_cleanup_method)
                        }

        try:
            x = requests.post(self.url, json=det_json_obj)
            print(x.text)
        except:
            pass

    def detection_controller(self, image_np):
        detections = self.make_detections(image_np)
        boundary_boxes = self.bndbox(image_np, detections)

        try:
            confidence_score = detections['detection_scores'][0]
            #cleaned = false

            if confidence_score > self.threshold:
                # ensure we are looking at different detecion object -- future update
                # if so create detection object
                # call logging function()
                self.logging_detection(detections, boundary_boxes)

            return boundary_boxes

        except IndexError:  # if there is no object in frame to detect
            return boundary_boxes


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
