"""
Grade model for storing Canvas grade information.
"""

from sqlalchemy import Column, String, Text, DateTime, Numeric, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel


class Grade(BaseModel):
    """Model for Canvas grades."""
    
    __tablename__ = 'grades'
    
    # Primary key - auto-incrementing integer
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign keys
    course_id = Column(String(50), ForeignKey('courses.id'), nullable=False)
    assignment_id = Column(String(50), ForeignKey('assignments.id'), nullable=False)
    
    # Grade information
    score = Column(Numeric(10, 2))
    grade = Column(String(10))  # Letter grade or percentage
    feedback = Column(Text)
    graded_at = Column(DateTime)
    
    # Relationships
    course = relationship("Course", back_populates="grades")
    assignment = relationship("Assignment", back_populates="grades")
    
    def validate(self):
        """Validate grade data."""
        if not self.course_id or not self.course_id.strip():
            raise ValueError("Course ID is required")
        
        if not self.assignment_id or not self.assignment_id.strip():
            raise ValueError("Assignment ID is required")
        
        if self.score is not None and self.score < 0:
            raise ValueError("Score cannot be negative")
        
        if self.grade and len(self.grade) > 10:
            raise ValueError("Grade must be 10 characters or less")
    
    @property
    def percentage(self):
        """Calculate percentage if score and assignment points are available."""
        if self.score is not None and self.assignment and self.assignment.points_possible:
            return (float(self.score) / float(self.assignment.points_possible)) * 100
        return None
    
    def __repr__(self):
        return f"<Grade(id={self.id}, assignment_id={self.assignment_id}, score={self.score}, grade={self.grade})>"