from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import numpy as np
import cv2
import uvicorn
from DetectionModel import DetectionModel
app = FastAPI()

LABEL_MAP_NAME = 'Tensorflow/workspace/annotations/label_map.pbtxt'
d2PathCkpt = '/Users/williamdoyle/Desktop/ssd_mobnet640'
d2Config = '/Users/williamdoyle/Desktop/ssd_mobnet640/pipeline.config'

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        #load model
        detection_model = DetectionModel(LABEL_MAP_NAME, d2PathCkpt, d2Config)
        while True:
            
            #Handle Feed
            contents = await websocket.receive_bytes()
            arr = np.frombuffer(contents, np.uint8)
            # await websocket.send_bytes(contents)
            frame = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)

            image_np = np.array(frame)

            # # #Model Interaction 
            frame = detection_model.detection_controller(image_np)
            
            #Cast Feed
            await websocket.send_bytes(contents)
            # await websocket.send_bytes(frame.tobytes())
            # np.to
            # frame = np.ndarray.tobytes(frame)
            # frame = frame.tobytes()
            # await websocket.send_bytes(frame.tobytes('A'))
        
            # cv2.imshow('object detection',  cv2.resize(frame, (800, 800))) 
            # cv2.waitKey(1)


    except WebSocketDisconnect:
        cv2.destroyWindow("frame")
        print("Client disconnected") 

if __name__ == '__main__':
    uvicorn.run("casting:app", reload=True, port=8080)

#take in video streams
#manage streams sent to detection api 
#output bndbox stream to web gui

