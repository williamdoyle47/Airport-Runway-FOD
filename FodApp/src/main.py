import uvicorn
import threading
import numpy as np
import cv2
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.websockets import WebSocketState
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import ORJSONResponse, StreamingResponse
from detection_modules.DetectionModel import DetectionModel
from fastapi.middleware.cors import CORSMiddleware
from data_modules import models
from data_modules import engine, SessionLocal
from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from data_modules.models import FOD
from fastapi.encoders import jsonable_encoder


# init detection model
detection_model = DetectionModel()
lock = threading.Lock()

# fast api settings
app = FastAPI()

# creates DB and table if does not exist
models.Base.metadata.create_all(bind=engine)

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
    directory="/Users/williamdoyle/Documents/GitHub/Airport-Runway-FOD/FodApp/src/ui/templates")
app.mount("/static", StaticFiles(directory="/Users/williamdoyle/Documents/GitHub/Airport-Runway-FOD/FodApp/src/ui/static"), name="static")

# routes


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/cameras")  # route for testing BE to FE connection
def camera_testing(request: Request):
    return templates.TemplateResponse("cameras.html", {"request": request})


@app.get("/cams")  # route to show multicam feature
def multi_camera_view(request: Request):
    return templates.TemplateResponse("cams.html", {"request": request})


@app.get('/video_feed')
def video_feed():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')


def gen_frames():
    camera = cv2.VideoCapture(1)
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

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Model Interaction
            frame = detection_model.detection_controller(image_np)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    camera.release()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    while True:
        try:
            command = await websocket.receive_text()
            if str(command) == "open":
                # await asyncio.sleep(5)
                obj = db.query(models.FOD).order_by(
                    models.FOD.id.desc()).first()
                json_compatible_item_data = jsonable_encoder(obj)
                print(type(json_compatible_item_data))
                await websocket.send_json(json_compatible_item_data)

        except WebSocketDisconnect:
            print("Socket Disconnected")


# return reports template
# @app.get("/reports")

# Connect to reporting routes


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


FODS = []


@app.get("/all_logs")
def logs(db: Session = Depends(get_db)):
    return (db.query(models.FOD).all())


@app.get("/all_uncleaned")
async def all_uncleaned_fod(db: Session = Depends(get_db)):
    return db.query(models.FOD).filter(models.FOD.cleaned == False).all()


@app.get("/fod_img/{fod_uuid}")
async def fod_img(fod_uuid: str):
    return FileResponse("/Users/williamdoyle/Documents/GitHub/Airport-Runway-FOD/FodApp/src/data_modules/detectionImages/" + fod_uuid + ".jpg")
    # need to make this path dynamic in future update


@app.get("/fod/{fod_uuid}")
async def fod_by_uuid(fod_uuid: str, db: Session = Depends(get_db)):
    return db.query(models.FOD).filter(models.FOD.uuid == str(fod_uuid)).first()


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


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
