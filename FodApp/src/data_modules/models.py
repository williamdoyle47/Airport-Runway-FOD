from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from data_modules.database import Base


class FOD(Base):
    __tablename__ = "fod_logs"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String)
    fod_type = Column(String)
    timestamp = Column(DateTime)
    coord = Column(String)
    confidence_level = Column(Float)
    image_path = Column(String)
    cleaned = Column(Boolean, default=False)
    recommended_action = Column(String)
    cleaned_timestamp = Column(
        DateTime, nullable=True)
