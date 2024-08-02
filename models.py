from sqlalchemy import Column, Integer, String, Text, ForeignKey, ARRAY, DateTime, func, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Caregiver model
class Caregiver(Base):
    __tablename__ = "caregivers"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    phone = Column(String(15), nullable=False)
    address = Column(String(100), nullable=False)

    points = Column(Integer)

    # Define relationship to caregiver_profiles table
    profiles = relationship("CaregiverProfile", back_populates="caregiver")

class CaregiverProfile(Base):
    __tablename__ = 'caregiver_profiles'
    
    id = Column(Integer, primary_key=True, index=True)
    caregiver_id = Column(Integer, ForeignKey('caregivers.id'), nullable=False)  # ForeignKey 설정 추가
    experience_ids = Column(ARRAY(Integer), nullable=False)
    desired_hourly_rate = Column(Integer)
    activity_start_time = Column(DateTime(timezone=True))  # TIMESTAMPTZ
    activity_end_time = Column(DateTime(timezone=True))    # TIMESTAMPTZ

    # Define relationship to caregivers table
    caregiver = relationship("Caregiver", back_populates="profiles")




class Guardian(Base):
    __tablename__ = "guardians"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    phone = Column(String(15), nullable=False)
    address = Column(String(100), nullable=False)

    points = Column(Integer)
    relationship_index = Column(Integer, ForeignKey('relationship.id'))
    service_urgency_index = Column(Integer, nullable=False)

# class Relationship(Base):
#     __tablename__ = "relationship"

#     id = Column(Integer, primary_key=True, index=True)
#     relationship_type = Column(String(50), unique=True, index=True)

class Relationship(Base):
    __tablename__ = 'relationship'

    id = Column(Integer, primary_key=True, index=True)
    relationship_type = Column(String(50), unique=True, index=True)

    def __repr__(self):
        return f"<Relationship(id={self.id}, relationship_type='{self.relationship_type}')>"
    

# Message 모델
class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    sender_username = Column(String(50), nullable=False)
    receiver_username = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)



class Caregiving(Base):
    __tablename__ = 'caregiving'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)

    start_date = Column(TIMESTAMP, nullable=False)
    end_date = Column(TIMESTAMP, nullable=False)
    care_days = Column(ARRAY(String), nullable=True)

    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)

    extra_days = Column(ARRAY(TIMESTAMP), nullable=True)
    address = Column(String(255), nullable=False)

    medications = Column(ARRAY(String), nullable=True)
    note = Column(Text, nullable=True)
    
    urgent_fee = Column(Integer, nullable=True)
    severe_fee = Column(Integer, nullable=True)