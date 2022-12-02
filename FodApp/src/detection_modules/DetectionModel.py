import numpy as np
import tensorflow as tf
import os
from detection_modules.DetectionLogging import LogDetection
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util

class DetectionModel:
    def __init__(self):
        self.label_map_name = "/Users/williamdoyle/Documents/GitHub/Airport-Runway-FOD/FodApp/src/Tensorflow/workspace/annotations/label_map.pbtxt"
        self.d2PathCkpt = '/Users/williamdoyle/Desktop/ssd_mobnet640'
        self.d2Config = '/Users/williamdoyle/Desktop/ssd_mobnet640/pipeline.config'
        self.load_model(self.label_map_name, self.d2PathCkpt, self.d2Config)
        

    def load_model(self, label_map_name, d2PathCkpt, d2Config):
        try:
            # Load pipeline config and build a detection model
            self.configs = config_util.get_configs_from_pipeline_file(d2Config)
            self.detection_model = model_builder.build(model_config=self.configs['model'], is_training=False)
            # Restore checkpoint
            self.ckpt = tf.compat.v2.train.Checkpoint(model=self.detection_model)
            self.ckpt.restore(os.path.join(d2PathCkpt, 'ckpt-11')).expect_partial() #ensure up to date with current checkpoint
            self.category_index = label_map_util.create_category_index_from_labelmap(label_map_name)
        except:
            print("Error loading model, check inputs")

    def detect_fn(self, input_tensor): #connects to TF API
        input_tensor, shapes = self.detection_model.preprocess(input_tensor)
        prediction_dict = self.detection_model.predict(input_tensor, shapes)
        detections = self.detection_model.postprocess(prediction_dict, shapes)
        return detections

    def make_detections(self, image_np):
        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
        detections = self.detect_fn(input_tensor)
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                            for key, value in detections.items()}
        detections['num_detections'] = num_detections
        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
        
        return detections

    
    def bndbox(self, image_np, detections):
        label_id_offset = 1

        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np,
            detections['detection_boxes'],
            detections['detection_classes'] + label_id_offset,
            detections['detection_scores'],
            self.category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=5,
            min_score_thresh=.6,
            agnostic_mode=False)
        return image_np

    #Log interactions 
    def logging_detection(self, Detection):
        log_controller = LogDetection(Detection)
        log_controller.log_fod()

    def detection_controller(self, image_np):
        detections = self.make_detections(image_np)
        boundary_boxes = self.bndbox(image_np,detections)

        # fod_type = self.category_index[detections['detection_classes'][0]+1]["name"]
        # confidence_score = detections['detection_scores'][0] * 100

        # threshold = 60
        # if confidence_score > threshold:
        #     detection = Detection(fod_type,"[0,0]",datetime.datetime.now(),float(confidence_score))
        #     self.logging_detection(detection)


        #ensure we are looking at different detecion
            #if so create detection object
            #call logging function()
            #recommend action() + send notification

        #dist est. function

        return boundary_boxes