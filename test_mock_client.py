#!/usr/bin/env python3
"""
Test script for MockCanvasClient to verify all functionality works correctly.
"""

from mcp_server.mock_canvas_client import MockCanvasClient


def test_mock_client():
    """Test all MockCanvasClient methods."""
    print("=" * 60)
    print("Testing MockCanvasClient")
    print("=" * 60)

    client = MockCanvasClient()

    # Test 1: Get student by login
    print("\n1. Testing get_student_by_login...")
    student = client.get_student_by_login('alex@example.edu')
    assert student is not None, "Student not found"
    print(f"   ✓ Found student: {student['name']} ({student['login']})")

    # Test 2: Get courses for student
    print("\n2. Testing get_courses_for_student...")
    courses = client.get_courses_for_student(student['id'])
    assert len(courses) > 0, "No courses found"
    print(f"   ✓ Found {len(courses)} courses:")
    for course in courses:
        print(f"     - {course['name']} ({course['code']})")

    # Test 3: Get upcoming assignments
    print("\n3. Testing get_upcoming_assignments_for_student...")
    upcoming = client.get_upcoming_assignments_for_student(student['id'], 30)
    print(f"   ✓ Found {len(upcoming)} upcoming assignments:")
    for assignment in upcoming[:3]:  # Show first 3
        print(f"     - {assignment['title']}")
        print(f"       Due: {assignment['due_date']}")
        print(f"       Course: {assignment.get('course_name', 'N/A')}")
        print(f"       Status: {assignment.get('submission_status', 'N/A')}")

    # Test 4: Get missing assignments
    print("\n4. Testing get_missing_assignments_for_student...")
    missing = client.get_missing_assignments_for_student(student['id'])
    print(f"   ✓ Found {len(missing)} missing assignments:")
    for assignment in missing:
        print(f"     - {assignment['title']}")
        print(f"       Days overdue: {assignment.get('days_overdue', 'N/A')}")
        print(f"       Course: {assignment.get('course_name', 'N/A')}")

    # Test 5: Get course grades
    print("\n5. Testing get_course_grades_for_student...")
    grades = client.get_course_grades_for_student(student['id'])
    print(f"   ✓ Found {len(grades)} course grades:")
    for grade in grades:
        score = grade.get('current_score')
        score_str = f"{score:.1f}%" if score is not None else "N/A"
        letter = grade.get('letter_grade', 'N/A')
        print(
            f"     - {grade.get('course_name', 'N/A')}: {score_str} ({letter})")

    # Test 6: Get assignment grades
    print("\n6. Testing get_assignment_grades_for_student...")
    assignment_grades = client.get_assignment_grades_for_student(student['id'])
    print(f"   ✓ Found {len(assignment_grades)} graded assignments:")
    for grade in assignment_grades:
        print(f"     - {grade.get('assignment_title', 'N/A')}")
        print(
            f"       Score: {grade.get('score', 'N/A')}/{grade.get('points_possible', 'N/A')}")
        print(f"       Grade: {grade.get('grade', 'N/A')}")

    # Test 7: Get announcements
    print("\n7. Testing get_announcements_for_student...")
    announcements = client.get_announcements_for_student(
        student['id'], limit=5)
    print(f"   ✓ Found {len(announcements)} announcements:")
    for announcement in announcements[:3]:  # Show first 3
        print(f"     - {announcement['title']}")
        print(f"       Course: {announcement.get('course_name', 'N/A')}")
        print(f"       Posted: {announcement['posted_date']}")

    # Test 8: Get course assignments
    print("\n8. Testing get_assignments_for_course...")
    if courses:
        course_id = courses[0]['id']
        course_assignments = client.get_assignments_for_course(course_id)
        print(
            f"   ✓ Found {len(course_assignments)} assignments for {courses[0]['name']}:")
        for assignment in course_assignments:
            print(f"     - {assignment['title']}")
            print(f"       Due: {assignment.get('due_date', 'N/A')}")
            print(f"       Points: {assignment.get('points_possible', 'N/A')}")

    print("\n" + "=" * 60)
    print("✓ All tests passed successfully!")
    print("=" * 60)
    print("\nMockCanvasClient is ready to use with the MCP server.")
    print("Test logins: alex@example.edu, jordan@example.edu")


if __name__ == "__main__":
    try:
        test_mock_client()
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
