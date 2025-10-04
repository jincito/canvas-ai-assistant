from fastapi import APIRouter
from typing import List

router = APIRouter(
    prefix="/assignments",
    tags=["Assignments"]
)

# Temporary mock data
mock_assignments = [
    {"id": 1, "title": "Capstone Proposal", "due_date": "2025-10-15"},
    {"id": 2, "title": "Database Homework", "due_date": "2025-10-20"}
]

@router.get("/", summary="Fetch upcoming assignments")
def get_assignments() -> List[dict]:
    return {"assignments": mock_assignments}
