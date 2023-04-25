import uvicorn
import threading
import numpy as np
import cv2
import json
import pathlib
import asyncio

# starlette and fast api imports
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from sse_starlette.sse import EventSourceResponse

# sqlalchemy imports
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

# FodApp Imports
from detection_modules.DetectionModel import DetectionModel
from data_modules import models
from data_modules import engine, SessionLocal
from data_modules.models import FOD
from data_modules.generate_csv import *
from gps_controller import GPS_Controller

# init detection model
detection_model = DetectionModel()
gps_controller = GPS_Controller()
lock = threading.Lock()

# fast api settings
app = FastAPI()

# creates DB and table if does not exist
models.Base.metadata.create_all(bind=engine)

MESSAGE_STREAM_DELAY = 1  # second
MESSAGE_STREAM_RETRY_TIMEOUT = 15000  # milisecond

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# mount relevant dirs -- clean upo
templates = Jinja2Templates(
    directory=pathlib.Path(__file__).parent.resolve().joinpath('ui', 'templates'))
app.mount("/static", StaticFiles(directory=pathlib.Path(__file__)
          .parent.resolve().joinpath('ui', 'static')), name="static")

# routes


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/offline")
def home(request: Request):
    return templates.TemplateResponse("map.html", {"request": request})


@app.get("/reports")  # route to show multicam feature
def multi_camera_view(request: Request):
    return templates.TemplateResponse("reports.html", {"request": request})


@app.get('/stream')
async def message_stream(request: Request, db: Session = Depends(get_db)):
    latest_detections = []
    obj = db.query(models.FOD).order_by(
        models.FOD.id.desc()).first()
    json_compatible_item_data = jsonable_encoder(obj)
    json_compatible_item_data = json.dumps(json_compatible_item_data)
    latest_detections.append(json_compatible_item_data)

    def new_messages():
        obj = db.query(models.FOD).order_by(
            models.FOD.id.desc()).first()
        json_compatible_item_data = jsonable_encoder(obj)
        json_compatible_item_data = json.dumps(json_compatible_item_data)
        if json_compatible_item_data != latest_detections[-1]:
            latest_detections.append(json_compatible_item_data)
            return json_compatible_item_data
        else:
            return None

    async def event_generator():
        while True:
            # If client was closed the connection
            if await request.is_disconnected():
                break

            # Checks for new messages and return them to client if any
            item = new_messages()
            if item:
                yield {
                    "event": "update",
                    "id": "message_id",
                    "retry": MESSAGE_STREAM_RETRY_TIMEOUT,
                    "data": f"{item}"
                }

            await asyncio.sleep(MESSAGE_STREAM_DELAY)

    return EventSourceResponse(event_generator())


@app.get('/video_feed')
def video_feed():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')


def gen_frames():
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        with lock:
            success, frame = camera.read()
            if not success:
                camera.release()
                print("Not success")
                break
            else:
                image_np = np.array(frame)

            # Model Interaction
            frame = detection_model.detection_controller(
                image_np, gps_controller)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    camera.release()


############### SEPERATE LATER ##########

class FOD(BaseModel):
    timestamp: datetime = Field(default=datetime.now())
    uuid: str = Field()
    fod_type: str = Field(min_length=1)
    coord: str = Field(min_length=1, max_length=50)
    confidence_level: float = Field(gt=0, lt=101)
    image_path: str = Field(min_length=0, max_length=100)
    cleaned: bool = Field(default=False)
    recommended_action: str = Field(min_length=1, max_length=100)
    cleaned_timestamp: datetime = Field(default=None)

# Basic Fod Routes


@app.get("/all_logs")
def logs(db: Session = Depends(get_db)):
    return (db.query(models.FOD).all())


@app.get("/all_uncleaned")
async def all_uncleaned_fod(db: Session = Depends(get_db)):
    return db.query(models.FOD).filter(models.FOD.cleaned == False).all()


@app.get("/fod_img/{fod_uuid}")
async def fod_img(fod_uuid: str):
    fod_uuid_full = fod_uuid + ".jpg"
    return FileResponse(pathlib.Path(__file__).parent.resolve().joinpath('data_modules', 'detectionImages', fod_uuid_full))


@app.get("/fod/{fod_uuid}")
async def fod_by_uuid(fod_uuid: str, db: Session = Depends(get_db)):
    return db.query(models.FOD).filter(models.FOD.uuid == str(fod_uuid)).first()


@app.get("/get_gps_status")
async def gps_status():
    status = gps_controller.get_gps_status()
    if status:
        coord_str = gps_controller.extract_coordinates()
        return {"status": "on", "current_coords": coord_str}
    else:
        return {"status": "off"}


@app.patch("/toggle_gps")
async def toggle_gps():
    gps_controller.toggle_device()
    status = gps_controller.get_gps_status()
    coord_str = gps_controller.extract_coordinates()
    if status:
        print(gps_controller.extract_coordinates())
        return {"status": "on", "current_coords": coord_str}
    else:
        return {"status": "off"}


@app.post("/add_fod")
async def create_log(fod: FOD, db: Session = Depends(get_db)):
    log_model = models.FOD()
    log_model.fod_type = fod.fod_type
    log_model.uuid = fod.uuid
    log_model.timestamp = datetime.now()
    log_model.coord = fod.coord
    log_model.confidence_level = fod.confidence_level
    log_model.image_path = fod.image_path
    log_model.cleaned = fod.cleaned
    log_model.recommended_action = fod.recommended_action
    log_model.cleaned_timestamp = None

    db.add(log_model)
    db.commit()
    return fod


@app.patch("/mark_clean/{fod_uuid}")
def mark_fod_clean(fod_uuid: str, db: Session = Depends(get_db)):
    try:
        fod_uuid = fod_uuid.replace('uuid=', '')
        FOD = db.query(models.FOD).filter(
            models.FOD.uuid == str(fod_uuid)).first()
        if FOD is None:
            raise HTTPException(status_code=404, detail="Fod uuid not found")
        FOD.cleaned = True
        FOD.cleaned_timestamp = datetime.now()
        db.commit()
        return 200

    except:
        print("Error Occured")


@app.delete('/{log_id}')
def delete_log(log_id: int, db: Session = Depends(get_db)):
    log_model = db.query(models.Logs).filter(models.Logs.id == log_id).first()
    if log_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {log_id} : Does not exist"
        )

    db.query(models.Logs).filter(models.Logs.id == log_id).delete()

    db.commit()


# Reports Routes


@app.get("/common_fod_type")
def logs(db: Session = Depends(get_db)):
    results = db.query(models.FOD).all()
    typ_arr = []
    for r in results:
        typ_arr.append(r.fod_type)
        # print(r.fod_type)
    common = max(set(typ_arr), key=typ_arr.count)

    return common


@app.get("/total_unclean")
def logs(db: Session = Depends(get_db)):
    results = db.query(models.FOD).all()
    typ_arr = []
    for r in results:
        if (r.cleaned == False):
            typ_arr.append(r.fod_type)
        # print(r.fod_type)

    return len(typ_arr)


@app.get("/avg_cleanup_time")
def logs(db: Session = Depends(get_db)):
    results = db.query(models.FOD).all()
    cleanup_arr = []
    for r in results:
        if r.cleaned_timestamp != None:
            time_diff = r.cleaned_timestamp - r.timestamp
            cleanup_arr.append(time_diff)
            # print(time_diff)
    average_timedelta = sum(
        cleanup_arr, timedelta(0)) / len(cleanup_arr)
    average_timedelta = str(average_timedelta)
    return average_timedelta


@app.get("/common_location")
def logs(db: Session = Depends(get_db)):
    results = db.query(models.FOD).all()
    coords_arr = []
    for r in results:
        coords_arr.append(r.coord)
    common = max(set(coords_arr), key=coords_arr.count)

    # prints points and occurence of fod at that point.
    # for x in set(coords_arr):
    #     print(x, coords_arr.count(x))
    # data = x,coords_arr.count(x)
    # # print(data)

    return common


# Create CSV file
@app.get("/generate_csv")
def create_csv():
    generate_fod_csv()

    return ("Fod CSV file generated")


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
