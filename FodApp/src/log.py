from datetime import datetime
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from data_modules import models
from data_modules import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
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

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Log(BaseModel):
    # dt: datetime = None
    timestamp: datetime = Field(datetime.now())
    fod_type: str = Field(min_length=1)
    coord: str = Field(min_length=1, max_length=50)
    confidence_level: float = Field(gt=0, lt=101)
    image_path: str = Field(min_length=0, max_length=100)
    recommended_action: str = Field(min_length=1, max_length=100)
LOGS = []




templates = Jinja2Templates(directory="/Users/williamdoyle/Documents/GitHub/Airport-Runway-FOD/FodApp/src/ui/templates")
app.mount("/static", StaticFiles(directory="/Users/williamdoyle/Documents/GitHub/Airport-Runway-FOD/FodApp/src/ui/static"), name="static")



# pages
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/cameras")
def home(request: Request):
    return templates.TemplateResponse("cameras.html", {"request": request})

@app.get("/cams")
def home(request: Request):
    return templates.TemplateResponse("cams.html", {"request": request})
    
#logs
@app.get("/logs")
def logs(db: Session = Depends(get_db)):
    return (db.query(models.Logs).all())


@app.post("/logs")
def create_log(log: Log, db: Session = Depends(get_db)):
    log_model = models.Logs()
    # log_model.timestamp = log.timestamp
    log_model.fod_type = log.fod_type
    log_model.coord = log.coord
    log_model.confidence_level = log.confidence_level
    log_model.image_path = log.image_path
    log_model.recommended_action = log.recommended_action

    db.add(log_model)
    db.commit()
    return log

@app.put('/{log_id}')
def update_log(log_id: int, log: Log, db: Session = Depends(get_db)):
    log_model = db.query(models.Logs).filter(models.Logs.id == log_id).first()

    if log_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {log_id} : Does not exist"
        )
    log_model.fod_type = log.fod_type
    log_model.coord = log.coord
    log_model.confidence_level = log.confidence_level
    log_model.image_path = log.image_path
    log_model.recommended_action = log.recommended_action

    db.add(log_model)
    db.commit()

    return log

@app.delete('/{log_id}')
def delete_log(log_id: int, db: Session = Depends(get_db) ):
    log_model = db.query(models.Logs).filter(models.Logs.id == log_id).first()
    if log_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {log_id} : Does not exist"
        )
    
    db.query(models.Logs).filter(models.Logs.id == log_id).delete()

    db.commit()



if __name__ == '__main__':
    uvicorn.run("log:app", reload=True)
