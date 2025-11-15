"""
RealCanvasClient - Canvas API client for production use.

This client will connect to the actual Canvas LMS API to fetch real student data.
Currently a placeholder for future implementation.
"""

from typing import Any, Dict, List, Optional
import requests


class RealCanvasClient:
    """
    Real Canvas API client (placeholder for future implementation).

    This class will implement the same interface as MockCanvasClient but will
    make actual API calls to Canvas LMS.
    """

    def __init__(self, canvas_url: str, api_token: str):
        """
        Initialize the Canvas API client.

        Args:
            canvas_url: Base URL for Canvas instance (e.g., https://canvas.instructure.com)
            api_token: Canvas API access token
        """
        self.canvas_url = canvas_url.rstrip('/')
        self.api_token = api_token
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }

    def get_student_by_login(self, login: str) -> Optional[Dict[str, Any]]:
        """Get student information by login/email."""
        raise NotImplementedError("Real Canvas client not yet implemented")

    def get_student_by_id(self, student_id: str) -> Optional[Dict[str, Any]]:
        """Get student information by ID."""
        raise NotImplementedError("Real Canvas client not yet implemented")

    def get_courses_for_student(self, student_id: str) -> List[Dict[str, Any]]:
        """Get all courses for a student."""
        raise NotImplementedError("Real Canvas client not yet implemented")

    def get_course_by_id(self, course_id: str) -> Optional[Dict[str, Any]]:
        """Get course information by ID."""
        raise NotImplementedError("Real Canvas client not yet implemented")

    def get_assignments_for_course(self, course_id: str) -> List[Dict[str, Any]]:
        """Get all assignments for a course."""
        raise NotImplementedError("Real Canvas client not yet implemented")

    def get_assignment_by_id(self, assignment_id: str) -> Optional[Dict[str, Any]]:
        """Get assignment by ID."""
        raise NotImplementedError("Real Canvas client not yet implemented")

    def get_upcoming_assignments_for_student(
        self,
        student_id: str,
        within_days: int = 7
    ) -> List[Dict[str, Any]]:
        """Get upcoming assignments for a student within specified days."""
        raise NotImplementedError("Real Canvas client not yet implemented")

    def get_missing_assignments_for_student(self, student_id: str) -> List[Dict[str, Any]]:
        """Get missing/overdue assignments for a student."""
        raise NotImplementedError("Real Canvas client not yet implemented")

    def get_course_grades_for_student(self, student_id: str) -> List[Dict[str, Any]]:
        """Get grade summaries for all courses a student is enrolled in."""
        raise NotImplementedError("Real Canvas client not yet implemented")

    def get_assignment_grades_for_student(
        self,
        student_id: str,
        course_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get individual assignment grades for a student."""
        raise NotImplementedError("Real Canvas client not yet implemented")

    def get_announcements_for_student(
        self,
        student_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get recent announcements for all courses a student is enrolled in."""
        raise NotImplementedError("Real Canvas client not yet implemented")

    def get_announcements_for_course(
        self,
        course_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get announcements for a specific course."""
        raise NotImplementedError("Real Canvas client not yet implemented")
