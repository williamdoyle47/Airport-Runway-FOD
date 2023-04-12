import numpy as np
import requests
import sys
sys.path.insert(0,"..")
from PIL import Image
from detection_modules.DetectionModel import DetectionModel
  #code for testing
#if __name__ == '__main__':
def detection_test():
    image_raw = Image.open('detection_test.jpg')
    det = DetectionModel()
    image_np = np.asarray(image_raw, dtype=np.uint8)
    frame = det.detection_controller(image_np)
    response = requests.get('http://127.0.0.1:8000/common_fod_type')
    #print(response.status_code())
    assert response.status_code() is 200
#need bater way to validate
#need way to flasely load into analytics