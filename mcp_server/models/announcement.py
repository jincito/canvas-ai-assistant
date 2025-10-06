"""
Announcement model for storing Canvas announcement information.
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class Announcement(BaseModel):
    """Model for Canvas announcements."""
    
    __tablename__ = 'announcements'
    
    # Primary key - Canvas announcement ID
    id = Column(String(50), primary_key=True)
    
    # Foreign key to course
    course_id = Column(String(50), ForeignKey('courses.id'), nullable=False)
    
    # Announcement information
    title = Column(String(255), nullable=False)
    content = Column(Text)
    posted_date = Column(DateTime, nullable=False)
    
    # Relationships
    course = relationship("Course", back_populates="announcements")
    
    def validate(self):
        """Validate announcement data."""
        if not self.title or not self.title.strip():
            raise ValueError("Announcement title is required")
        
        if len(self.title) > 255:
            raise ValueError("Announcement title must be 255 characters or less")
        
        if not self.course_id or not self.course_id.strip():
            raise ValueError("Course ID is required")
        
        if not self.posted_date:
            raise ValueError("Posted date is required")
    
    def __repr__(self):
        return f"<Announcement(id={self.id}, title={self.title}, course_id={self.course_id}, posted_date={self.posted_date})>"