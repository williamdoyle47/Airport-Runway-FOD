import uvicorn
import cv2
import threading
import numpy as np
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import ORJSONResponse, StreamingResponse
from detection_modules import DetectionModel
from fastapi.middleware.cors import CORSMiddleware
from data_modules import models
from data_modules import engine, SessionLocal
from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from detection_modules.DetectionModel import DetectionModel

detection_model = DetectionModel()
lock = threading.Lock()
app = FastAPI()
camera = cv2.VideoCapture(1)
if not camera.isOpened():
    print("Cannot open camera")
    exit()

# templates = Jinja2Templates(directory="/Users/User/Documents/GitHub/Airport-Runway-FOD/FodApp/src/ui/templates")
# app.mount("/static", StaticFiles(directory="/Users/User/Documents/GitHub/Airport-Runway-FOD/FodApp/src/ui/static"), name="static")

def gen_frames():
    while True:
        with lock:
            success, frame = camera.read()
            if not success:
                print("Not success")
                break
            else:
                image_np = np.array(frame)
            # #Model Interaction 
                frame = detection_model.detection_controller(image_np)

                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("test_video.html", {"request": request})

@app.get('/video_feed')
def video_feed():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

# @app.websocket("/ws")
# async def get_stream(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             success, frame = camera.read()
#             if not success:
#                 break
#             else:
#                 ret, buffer = cv2.imencode('.jpg', frame)
#                 await websocket.send_bytes(buffer.tobytes())  
#     except WebSocketDisconnect:
#         print("Client disconnected")   
 
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)


if __name__ == '__main__':
    uvicorn.run("testing_camera_stream:app", reload=True)