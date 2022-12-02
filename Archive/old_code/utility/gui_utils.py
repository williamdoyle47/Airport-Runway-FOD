import cv2 as cv 
import time

from Archive.old_code.data_model_interactions import *
from Archive.old_code.gui_comp import *


# Camera Settings
camera_Width  = 480 # 320 # 480 # 720 # 1080 # 1620
camera_Height = 360 # 240 # 360 # 540 # 810  # 1215
frameSize = (camera_Width, camera_Height)
video_capture1 = cv.VideoCapture(0)
video_capture2 = cv.VideoCapture(1)
video_capture3 = cv.VideoCapture(2)
video_capture4 = cv.VideoCapture(3)
video_capture5 = cv.VideoCapture(4)
time.sleep(2.0)


def getThreshold(threshString): #returns threshold amount
    return int(threshString[:-1]) / 100

def getCameraAmount(cameraString): #returns camera amount to know how many cams to display
    return int(cameraString)

def getCameraChoice(choice): # returns the correct frame for camera display
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

def destory_camera_windows():
    video_capture1.release()
    video_capture2.release()
    video_capture3.release()
    video_capture4.release()
    video_capture5.release()
    cv.destroyAllWindows()

def selectCamera(cameraAmount, values, threshold, tracker, gps_controller, mapping, window):
    if cameraAmount == 1:
        ret, frame1 = getCameraChoice(values['choice1'])
        tfBoundingBoxes(frame1, "cam1", "cam1Update", threshold, frameSize, tracker, gps_controller, mapping, window)
    elif cameraAmount == 2:
        ret, frame1 = getCameraChoice(values['choice1'])
        tfBoundingBoxes(frame1, "cam1", "cam1Update", threshold, frameSize, tracker, gps_controller, mapping, window)
        ret, frame2 = getCameraChoice(values['choice2'])
        tfBoundingBoxes(frame2, "cam2", "cam2Update", threshold, frameSize, tracker, gps_controller, mapping, window)
    elif cameraAmount == 3:
        ret, frame1 = getCameraChoice( values['choice1'])
        tfBoundingBoxes(frame1, "cam1", "cam1Update", threshold, frameSize, tracker, gps_controller, mapping, window)
        ret, frame2 = getCameraChoice(values['choice2'])
        tfBoundingBoxes(frame2, "cam2", "cam2Update", threshold, frameSize, tracker, gps_controller, mapping, window)
        ret, frame3 = getCameraChoice(values['choice3'])
        tfBoundingBoxes(frame3, "cam3", "cam3Update", threshold, frameSize, tracker, gps_controller, mapping, window)
    elif cameraAmount == 4:
        ret, frame1 = getCameraChoice(values['choice1'])
        tfBoundingBoxes(frame1, "cam1", "cam1Update", threshold, frameSize, tracker, gps_controller, mapping, window)
        ret, frame2 = getCameraChoice(values['choice2'])
        tfBoundingBoxes(frame2, "cam2", "cam2Update", threshold, frameSize, tracker, gps_controller, mapping, window)
        ret, frame3 = getCameraChoice(values['choice3'])
        tfBoundingBoxes(frame3, "cam3", "cam3Update", threshold, frameSize, tracker, gps_controller, mapping, window)
        ret, frame4 = getCameraChoice(values['choice4'])
        tfBoundingBoxes(frame4, "cam4", "cam4Update", threshold, frameSize, tracker, gps_controller, mapping, window)
    elif cameraAmount == 5:
        ret, frame1 = getCameraChoice(values['choice1'])
        tfBoundingBoxes(frame1, "cam1", "cam1Update", threshold, frameSize, tracker, gps_controller, mapping, window)
        ret, frame2 = getCameraChoice(values['choice2'])
        tfBoundingBoxes(frame2, "cam2", "cam2Update", threshold, frameSize, tracker, gps_controller, mapping, window)
        ret, frame3 = getCameraChoice(values['choice3'])
        tfBoundingBoxes(frame3, "cam3", "cam3Update", threshold, frameSize, tracker, gps_controller, mapping, window)
        ret, frame4 = getCameraChoice(values['choice4'])
        tfBoundingBoxes(frame4, "cam4", "cam4Update", threshold, frameSize, tracker, gps_controller, mapping, window)
        ret, frame5 = getCameraChoice(values['choice5'])
        tfBoundingBoxes(frame5, "cam5", "cam5Update", threshold, frameSize, tracker, gps_controller, mapping, window)