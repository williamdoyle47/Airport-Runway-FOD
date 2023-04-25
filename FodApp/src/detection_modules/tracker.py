# Author: "PySource"
# For educational use only
import math
from matplotlib import pyplot as plt
import cv2 as cv
import datetime
import requests
import uuid
from object_detection.utils import label_map_util
import pathlib
from PIL import Image
from detection_modules.coords import coords, magnet, sweeping, rumble_strips, fod_containers
import random


class EuclideanDistTracker:

    detections_list = []

    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        self.url = "http://127.0.0.1:8000/add_fod"
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0

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

    def getDetectionsList(self):
        return self.detections_list

    def update(self, objects_rect, category_index, detections, frame, gps_controller):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
                # print(id, " ", dist)
                # Might need to change the dist < number based on speed
                if dist < 150:
                    self.center_points[id] = (cx, cy)
                    # print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object and save the image of the object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

                fod_uuid = uuid.uuid4()
                fod_uuid_full = str(fod_uuid) + '.jpg'

                # store fod images
                fod_type = category_index.get(
                    (detections['detection_classes'][0]))['name']
                # print(fod_type)  # get deteection class
                image_path = pathlib.Path(__file__).parents[1].resolve().joinpath(
                    'data_modules/detectionImages', fod_uuid_full)
                plt.imshow(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
                plt.savefig(image_path)

                # recommend actions
                rec_cleanup_method = self.recommend_action(fod_type)
                cleaned = False

                if gps_controller.get_gps_status() != None:
                    coor = gps_controller.extract_coordinates()
                    print(coor)
                    if coor == "0,0":
                        coor = random.choice(coords)
                    print(coor)
                else:
                    coor = random.choice(coords)

                image_path = "/detectionImages/" + \
                    str(fod_uuid) + '.jpg'  # fix this
                confidence_score = detections['detection_scores'][0]
                if confidence_score is None:
                    confidence_score = 0.0

                print(str(fod_type))

                # assign object
                det_json_obj = {"fod_type": str(fod_type),
                                "uuid": str(fod_uuid),
                                "coord": str(coor),
                                "confidence_level": float(confidence_score),
                                "image_path": str(image_path),
                                "cleaned": bool(cleaned),
                                "recommended_action": str(rec_cleanup_method)
                                }

                try:
                    x = requests.post(self.url, json=det_json_obj)
                    # print(x.text)
                except:
                    pass

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids
