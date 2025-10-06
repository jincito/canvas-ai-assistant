"""
Assignment model for storing Canvas assignment information.
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Numeric, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import BaseModel


class AssignmentStatus(PyEnum):
    """Enumeration for assignment status values."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"
    GRADED = "graded"


class Assignment(BaseModel):
    """Model for Canvas assignments."""
    
    __tablename__ = 'assignments'
    
    # Primary key - Canvas assignment ID
    id = Column(String(50), primary_key=True)
    
    # Foreign key to course
    course_id = Column(String(50), ForeignKey('courses.id'), nullable=False)
    
    # Assignment information
    title = Column(String(255), nullable=False)
    description = Column(Text)
    due_date = Column(DateTime)
    points_possible = Column(Numeric(10, 2))
    status = Column(Enum(AssignmentStatus), default=AssignmentStatus.NOT_STARTED)
    
    # Relationships
    course = relationship("Course", back_populates="assignments")
    grades = relationship("Grade", back_populates="assignment", cascade="all, delete-orphan")
    
    def validate(self):
        """Validate assignment data."""
        if not self.title or not self.title.strip():
            raise ValueError("Assignment title is required")
        
        if len(self.title) > 255:
            raise ValueError("Assignment title must be 255 characters or less")
        
        if not self.course_id or not self.course_id.strip():
            raise ValueError("Course ID is required")
        
        if self.points_possible is not None and self.points_possible < 0:
            raise ValueError("Points possible cannot be negative")
        
        if self.due_date and self.due_date < datetime.utcnow():
            # This is a warning, not an error - assignments can have past due dates
            pass
    
    @property
    def is_overdue(self):
        """Check if assignment is overdue."""
        if not self.due_date:
            return False
        return datetime.utcnow() > self.due_date and self.status not in [AssignmentStatus.COMPLETED, AssignmentStatus.GRADED]
    
    def __repr__(self):
        return f"<Assignment(id={self.id}, title={self.title}, course_id={self.course_id}, due_date={self.due_date})>"