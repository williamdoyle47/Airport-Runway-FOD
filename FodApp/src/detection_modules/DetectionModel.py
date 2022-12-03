import numpy as np
import tensorflow as tf
import os
import cv2
import json
import random
from detection_modules.DetectionLogging import LogDetection
from PIL import Image
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import requests


class DetectionModel:
    def __init__(self):
        self.pathnumber = 1
        self.label_id_offset = 1
        self.threshold = .70
        self.url = "http://127.0.0.1:8000/add_fod"
        self.label_map_name = "/Users/williamdoyle/Documents/GitHub/Airport-Runway-FOD/FodApp/src/Tensorflow/workspace/annotations/label_map.pbtxt"
        self.d2PathCkpt = '/Users/williamdoyle/Desktop/ssd_mobnet640'
        self.d2Config = '/Users/williamdoyle/Desktop/ssd_mobnet640/pipeline.config'
        self.load_model(self.label_map_name, self.d2PathCkpt, self.d2Config)

    def load_model(self, label_map_name, d2PathCkpt, d2Config):
        try:
            # Load pipeline config and build a detection model
            self.configs = config_util.get_configs_from_pipeline_file(d2Config)
            self.detection_model = model_builder.build(
                model_config=self.configs['model'], is_training=False)
            # Restore checkpoint
            self.ckpt = tf.compat.v2.train.Checkpoint(
                model=self.detection_model)
            # ensure up to date with current checkpoint
            self.ckpt.restore(os.path.join(
                d2PathCkpt, 'ckpt-11')).expect_partial()
            self.category_index = label_map_util.create_category_index_from_labelmap(
                label_map_name)
        except:
            print("Error loading model, check inputs")

    def detect_fn(self, input_tensor):  # connects to TF API
        input_tensor, shapes = self.detection_model.preprocess(input_tensor)
        prediction_dict = self.detection_model.predict(input_tensor, shapes)
        detections = self.detection_model.postprocess(prediction_dict, shapes)
        return detections

    def make_detections(self, image_np):
        input_tensor = tf.convert_to_tensor(
            np.expand_dims(image_np, 0), dtype=tf.float32)
        detections = self.detect_fn(input_tensor)
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                      for key, value in detections.items()}
        detections['num_detections'] = num_detections
        # detection_classes should be ints.
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

    def bndcoords(self, image_np, detections):
        im = Image.fromarray(image_np)
        im_width = im.width
        im_height = im.height
        xmin, ymin, xmax, ymax = detections['detection_boxes'][0]
        (x, x2, y, y2) = (xmin * im_width, xmax *
                          im_width, ymin * im_height, ymax * im_height)
        w = x2-x
        h = y2-y
        return x, y, w, h

    # Log interactions
    def logging_detection(self, Detection):
        log_controller = LogDetection()
        # add fod to db -- post request
        log_controller.log_fod()

    def detection_controller(self, image_np):
        detections = self.make_detections(image_np)
        boundary_boxes = self.bndbox(image_np, detections)
        try:
            confidence_score = detections['detection_scores'][0]
            #cleaned = false

            if confidence_score > self.threshold:

                fod_type = self.category_index.get(
                    (detections['detection_classes'][0] + self.label_id_offset))['name']
                image_path = "/Users/williamdoyle/Documents/GitHub/Airport-Runway-FOD/FodApp/src/data_modules/detectionImages" + \
                    str(self.pathnumber) + '.jpg'  # generalize

                cropped = Image.fromarray(boundary_boxes)
                cropped.save(image_path, 'JPEG')
                self.pathnumber += 1

                magnet = ['metal', 'screw']  # metallic objects
                sweeping = ['pen', 'glove', 'cloth', 'LuggageTag']
                rumble_strips = ['']
                fod_containers = ['wood']

                cleaning_methods = [magnet, sweeping,
                                    rumble_strips, fod_containers]
                rec_cleanup_method = any(
                    fod_type in sublist for sublist in cleaning_methods)

                cleaned = False

                coords = [
                    '44.87462654456526, -93.23352374789656',

                    '44.88583814551953, -93.23506109382541',

                    '44.89137135265227, -93.20909505790712',

                    '44.87643483672227, -93.20789571538998',

                    '44.8724721221139, -93.23791428396207',

                    '44.89221842098514, -93.20940715281053',

                    '44.87974420507467, -93.21723957283892',

                    '44.87909010759127, -93.21013319768998',

                    '44.883046426535195, -93.22328360041249']

                coor = random.choice(coords)

                image_path = "../../data_modules/detectionImages/" + \
                    str(self.pathnumber) + '.jpg'

                det_json_obj = {'fod_type': str(fod_type),
                                'coord': str(coor),
                                'confidence_level': float(confidence_score),
                                'image_path': str(image_path),
                                'cleaned': bool(cleaned),
                                'recommended_action': str(rec_cleanup_method)
                                }
                x = requests.post(self.url, json=det_json_obj)
                print(x.text)

            # ensure we are looking at different detecion object -- future update
                # if so create detection object
                # call logging function()
                # recommend action() + send notification

            # dist est. function

            return boundary_boxes

        except IndexError:
            return boundary_boxes


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
