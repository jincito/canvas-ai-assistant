from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    course = Column(String, index=True)
    title = Column(String)
    due_date = Column(DateTime)
    points = Column(Integer)
    submitted = Column(Boolean, default=False)


class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    course = Column(String, index=True)
    title = Column(String)
    timestamp = Column(String)  # keep string format for simplicity
