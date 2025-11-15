"""
MockCanvasClient - A high-fidelity mock implementation of Canvas API client.

This client loads mock Canvas data from JSON and provides methods to query
courses, assignments, submissions, grades, and announcements without requiring
actual Canvas API access.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from pathlib import Path


class MockCanvasClient:
    """Mock Canvas API client that operates on local JSON data."""

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the mock client with data from JSON file.

        Args:
            data_path: Path to JSON file with mock data. If None, uses default location.
        """
        if data_path is None:
            # Default to mock_data/canvas_data.json relative to project root
            project_root = Path(__file__).parent.parent
            data_path = project_root / "mock_data" / "canvas_data.json"

        self.data_path = Path(data_path)
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        """Load mock data from JSON file."""
        try:
            with open(self.data_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Mock data file not found at {self.data_path}. "
                "Please ensure mock_data/canvas_data.json exists."
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in mock data file: {e}")

    def get_student_by_login(self, login: str) -> Optional[Dict[str, Any]]:
        """
        Get student information by login/email.

        Args:
            login: Student login or email

        Returns:
            Student dict or None if not found
        """
        for student in self.data.get("students", []):
            if student.get("login") == login or student.get("email") == login:
                return student.copy()
        return None

    def get_student_by_id(self, student_id: str) -> Optional[Dict[str, Any]]:
        """
        Get student information by ID.

        Args:
            student_id: Student ID

        Returns:
            Student dict or None if not found
        """
        for student in self.data.get("students", []):
            if student.get("id") == student_id:
                return student.copy()
        return None

    def get_courses_for_student(self, student_id: str) -> List[Dict[str, Any]]:
        """
        Get all courses for a student.

        Args:
            student_id: Student ID

        Returns:
            List of course dicts
        """
        student = self.get_student_by_id(student_id)
        if not student:
            return []

        course_ids = student.get("courses", [])
        courses = []

        for course in self.data.get("courses", []):
            if course.get("id") in course_ids:
                courses.append(course.copy())

        return courses

    def get_course_by_id(self, course_id: str) -> Optional[Dict[str, Any]]:
        """
        Get course information by ID.

        Args:
            course_id: Course ID

        Returns:
            Course dict or None if not found
        """
        for course in self.data.get("courses", []):
            if course.get("id") == course_id:
                return course.copy()
        return None

    def get_assignments_for_course(self, course_id: str) -> List[Dict[str, Any]]:
        """
        Get all assignments for a course.

        Args:
            course_id: Course ID

        Returns:
            List of assignment dicts
        """
        assignments = []
        for assignment in self.data.get("assignments", []):
            if assignment.get("course_id") == course_id:
                # Enrich with course info
                enriched = assignment.copy()
                course = self.get_course_by_id(course_id)
                if course:
                    enriched["course_name"] = course.get("name")
                    enriched["course_code"] = course.get("code")
                assignments.append(enriched)
        return assignments

    def get_assignment_by_id(self, assignment_id: str) -> Optional[Dict[str, Any]]:
        """
        Get assignment by ID.

        Args:
            assignment_id: Assignment ID

        Returns:
            Assignment dict or None if not found
        """
        for assignment in self.data.get("assignments", []):
            if assignment.get("id") == assignment_id:
                enriched = assignment.copy()
                course = self.get_course_by_id(assignment.get("course_id"))
                if course:
                    enriched["course_name"] = course.get("name")
                    enriched["course_code"] = course.get("code")
                return enriched
        return None

    def get_upcoming_assignments_for_student(
        self,
        student_id: str,
        within_days: int = 7
    ) -> List[Dict[str, Any]]:
        """
        Get upcoming assignments for a student within specified days.

        Args:
            student_id: Student ID
            within_days: Number of days to look ahead (default: 7)

        Returns:
            List of upcoming assignment dicts with course info
        """
        courses = self.get_courses_for_student(student_id)
        course_ids = [c["id"] for c in courses]

        now = datetime.utcnow()
        cutoff = now + timedelta(days=within_days)

        upcoming = []
        for assignment in self.data.get("assignments", []):
            if assignment.get("course_id") not in course_ids:
                continue

            due_date_str = assignment.get("due_date")
            if not due_date_str:
                continue

            try:
                due_date = datetime.fromisoformat(
                    due_date_str.replace('Z', '+00:00'))
                # Remove timezone info for comparison
                due_date = due_date.replace(tzinfo=None)

                if now <= due_date <= cutoff:
                    enriched = assignment.copy()
                    course = self.get_course_by_id(assignment.get("course_id"))
                    if course:
                        enriched["course_name"] = course.get("name")
                        enriched["course_code"] = course.get("code")

                    # Add submission status
                    submission = self._get_submission(
                        assignment["id"], student_id)
                    if submission:
                        enriched["submission_status"] = submission.get(
                            "workflow_state")
                        enriched["submitted_at"] = submission.get(
                            "submitted_at")
                    else:
                        enriched["submission_status"] = "not_submitted"
                        enriched["submitted_at"] = None

                    upcoming.append(enriched)
            except (ValueError, AttributeError):
                continue

        # Sort by due date
        upcoming.sort(key=lambda x: x.get("due_date", ""))
        return upcoming

    def get_missing_assignments_for_student(self, student_id: str) -> List[Dict[str, Any]]:
        """
        Get missing/overdue assignments for a student.

        Args:
            student_id: Student ID

        Returns:
            List of missing assignment dicts with course info
        """
        courses = self.get_courses_for_student(student_id)
        course_ids = [c["id"] for c in courses]

        now = datetime.utcnow()
        missing = []

        for assignment in self.data.get("assignments", []):
            if assignment.get("course_id") not in course_ids:
                continue

            due_date_str = assignment.get("due_date")
            if not due_date_str:
                continue

            try:
                due_date = datetime.fromisoformat(
                    due_date_str.replace('Z', '+00:00'))
                due_date = due_date.replace(tzinfo=None)

                # Check if overdue
                if due_date < now:
                    submission = self._get_submission(
                        assignment["id"], student_id)

                    # Missing if no submission or submission is marked as missing
                    if not submission or submission.get("workflow_state") == "missing":
                        enriched = assignment.copy()
                        course = self.get_course_by_id(
                            assignment.get("course_id"))
                        if course:
                            enriched["course_name"] = course.get("name")
                            enriched["course_code"] = course.get("code")

                        enriched["submission_status"] = "missing"
                        enriched["days_overdue"] = (now - due_date).days
                        missing.append(enriched)
            except (ValueError, AttributeError):
                continue

        # Sort by how overdue (most overdue first)
        missing.sort(key=lambda x: x.get("days_overdue", 0), reverse=True)
        return missing

    def get_course_grades_for_student(self, student_id: str) -> List[Dict[str, Any]]:
        """
        Get grade summaries for all courses a student is enrolled in.

        Args:
            student_id: Student ID

        Returns:
            List of course grade dicts with course info
        """
        grades = []

        for course_grade in self.data.get("course_grades", []):
            if course_grade.get("student_id") == student_id:
                enriched = course_grade.copy()
                course = self.get_course_by_id(course_grade.get("course_id"))
                if course:
                    enriched["course_name"] = course.get("name")
                    enriched["course_code"] = course.get("code")
                    enriched["term"] = course.get("term")
                grades.append(enriched)

        return grades

    def get_assignment_grades_for_student(
        self,
        student_id: str,
        course_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get individual assignment grades for a student.

        Args:
            student_id: Student ID
            course_id: Optional course ID to filter by

        Returns:
            List of grade dicts with assignment and course info
        """
        grades = []

        for grade in self.data.get("grades", []):
            if grade.get("student_id") != student_id:
                continue

            if course_id and grade.get("course_id") != course_id:
                continue

            enriched = grade.copy()

            # Add assignment info
            assignment = self.get_assignment_by_id(grade.get("assignment_id"))
            if assignment:
                enriched["assignment_title"] = assignment.get("title")
                enriched["points_possible"] = assignment.get("points_possible")
                enriched["course_name"] = assignment.get("course_name")
                enriched["course_code"] = assignment.get("course_code")

            grades.append(enriched)

        return grades

    def get_announcements_for_student(
        self,
        student_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recent announcements for all courses a student is enrolled in.

        Args:
            student_id: Student ID
            limit: Maximum number of announcements to return

        Returns:
            List of announcement dicts with course info
        """
        courses = self.get_courses_for_student(student_id)
        course_ids = [c["id"] for c in courses]

        announcements = []
        for announcement in self.data.get("announcements", []):
            if announcement.get("course_id") in course_ids:
                enriched = announcement.copy()
                course = self.get_course_by_id(announcement.get("course_id"))
                if course:
                    enriched["course_name"] = course.get("name")
                    enriched["course_code"] = course.get("code")
                announcements.append(enriched)

        # Sort by posted date (most recent first)
        announcements.sort(
            key=lambda x: x.get("posted_date", ""),
            reverse=True
        )

        return announcements[:limit]

    def get_announcements_for_course(
        self,
        course_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get announcements for a specific course.

        Args:
            course_id: Course ID
            limit: Maximum number of announcements to return

        Returns:
            List of announcement dicts
        """
        announcements = []
        for announcement in self.data.get("announcements", []):
            if announcement.get("course_id") == course_id:
                enriched = announcement.copy()
                course = self.get_course_by_id(course_id)
                if course:
                    enriched["course_name"] = course.get("name")
                    enriched["course_code"] = course.get("code")
                announcements.append(enriched)

        # Sort by posted date (most recent first)
        announcements.sort(
            key=lambda x: x.get("posted_date", ""),
            reverse=True
        )

        return announcements[:limit]

    def _get_submission(
        self,
        assignment_id: str,
        student_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Internal helper to get submission for an assignment and student.

        Args:
            assignment_id: Assignment ID
            student_id: Student ID

        Returns:
            Submission dict or None if not found
        """
        for submission in self.data.get("submissions", []):
            if (submission.get("assignment_id") == assignment_id and
                    submission.get("student_id") == student_id):
                return submission.copy()
        return None
