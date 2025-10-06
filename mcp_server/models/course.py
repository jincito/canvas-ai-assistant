"""
Course model for storing Canvas course information.
"""

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from .base import BaseModel


class Course(BaseModel):
    """Model for Canvas courses."""
    
    __tablename__ = 'courses'
    
    # Primary key - Canvas course ID
    id = Column(String(50), primary_key=True)
    
    # Course information
    name = Column(String(255), nullable=False)
    code = Column(String(50))
    term = Column(String(50))
    
    # Relationships
    assignments = relationship("Assignment", back_populates="course", cascade="all, delete-orphan")
    announcements = relationship("Announcement", back_populates="course", cascade="all, delete-orphan")
    grades = relationship("Grade", back_populates="course", cascade="all, delete-orphan")
    
    def validate(self):
        """Validate course data."""
        if not self.name or not self.name.strip():
            raise ValueError("Course name is required")
        
        if len(self.name) > 255:
            raise ValueError("Course name must be 255 characters or less")
        
        if self.code and len(self.code) > 50:
            raise ValueError("Course code must be 50 characters or less")
        
        if self.term and len(self.term) > 50:
            raise ValueError("Course term must be 50 characters or less")
    
    def __repr__(self):
        return f"<Course(id={self.id}, name={self.name}, code={self.code})>"