"""
Canvas API Sync Script
This script will be responsible for fetching data from Canvas API
and storing it in the database for the MCP server to use.
"""

import requests
from datetime import datetime
from tenacity import retry, wait_exponential, stop_after_attempt
from manager import DatabaseManager


class CanvasSync:
    def __init__(self, canvas_url, api_token):
        self.canvas_url = canvas_url.rstrip("/")  # remove trailing slash
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        self.db = DatabaseManager()  # use your existing DB manager

    # ---------- Helper ----------
    def _get(self, endpoint, params=None):
        """Generic GET request handler with error handling."""
        url = f"{self.canvas_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params or {})
        response.raise_for_status()
        return response.json()

    # ---------- Fetch Data ----------
    def fetch_courses(self):
        """Fetch all active courses for the authenticated user."""
        print("Fetching courses...")
        courses = self._get("/api/v1/courses")
        # You can filter for active ones if you want
        active_courses = [c for c in courses if c.get("workflow_state") == "available"]
        print(f" Found {len(active_courses)} active courses.")
        return active_courses

    def fetch_assignments(self, course_id):
        """Fetch all assignments for a given course."""
        print(f"Fetching assignments for course {course_id}...")
        assignments = self._get(f"/api/v1/courses/{course_id}/assignments")
        print(f" Found {len(assignments)} assignments.")
        return assignments

    def fetch_announcements(self, course_id):
        """Fetch all announcements for a given course."""
        print(f"Fetching announcements for course {course_id}...")
        announcements = self._get(f"/api/v1/announcements", params={"context_codes[]": f"course_{course_id}"})
        print(f" Found {len(announcements)} announcements.")
        return announcements

    def fetch_grades(self, course_id):
        """Fetch student submission data (grades) for a course."""
        print(f"Fetching grades for course {course_id}...")
        grades = self._get(f"/api/v1/courses/{course_id}/students/submissions")
        print(f" Found {len(grades)} grade entries.")
        return grades

    # ---------- Sync Orchestration ----------
    @retry(wait=wait_exponential(multiplier=2, min=2, max=10), stop=stop_after_attempt(5))
    def sync_all_data(self):
        """Main method to sync all Canvas data."""
        print(" Starting Canvas data synchronization...")
        try:
            courses = self.fetch_courses()
            for course in courses:
                course_id = course["id"]

                # Save course
                self.db.store_course(course)

                # Save assignments
                assignments = self.fetch_assignments(course_id)
                self.db.store_assignments(assignments)

                # Save announcements
                announcements = self.fetch_announcements(course_id)
                self.db.store_announcements(announcements)

                # Save grades
                grades = self.fetch_grades(course_id)
                self.db.store_grades(grades)

            # Update last sync timestamp in DB
            self.db.update_sync_status(datetime.now())
            print(" Canvas data synchronization completed successfully!")

        except Exception as e:
            print(f" Error during Canvas sync: {e}")
            raise  # Tenacity will handle retries


if __name__ == "__main__":
    # Example usage (replace URL and token with environment variables)
    CANVAS_URL = "https://canvas.instructure.com"
    API_TOKEN = "YOUR_CANVAS_ACCESS_TOKEN"

    sync = CanvasSync(CANVAS_URL, API_TOKEN)
    sync.sync_all_data()
