from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from data_modules.database import Base

class Logs(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    fod_type = Column(String)
    coord = Column(String)
    confidence_level = Column(Float)
    image_path = Column(String)
    recommended_action = Column(String)
