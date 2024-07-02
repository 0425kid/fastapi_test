from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Caregiver model
class Caregiver(Base):
    __tablename__ = "caregivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)  # Changed to String with appropriate length
    phone = Column(String(20), nullable=False)  # Renamed to match the database column
    address = Column(String(255), nullable=False)
    experience = Column(Text)
    desired_hourly_rate = Column(Integer, nullable=False)
