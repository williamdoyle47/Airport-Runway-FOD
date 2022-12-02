from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from data_modules import models
from data_modules import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

#instantiate 
models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Log(BaseModel):
    timestamp: datetime = Field(datetime.now())
    fod_type: str = Field(min_length=1)
    coord: str = Field(min_length=1, max_length=50)
    confidence_level: float = Field(gt=0, lt=101)
    image_path: str = Field(min_length=0, max_length=100)
    recommended_action: str = Field(min_length=1, max_length=100)
LOGS = []


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