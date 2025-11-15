"""
Canvas AI Assistant MCP Server

This MCP server provides tools for querying Canvas LMS data through
the Model Context Protocol, allowing AI assistants like Claude to
interact with Canvas course information, assignments, grades, and announcements.
"""

import os
import asyncio
from typing import Any, Optional
from datetime import datetime

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp import types

from .mock_canvas_client import MockCanvasClient


# Configuration flag for mock vs real Canvas client
USE_MOCK_CANVAS = os.getenv("USE_MOCK_CANVAS", "true").lower() == "true"

# Initialize the Canvas client
if USE_MOCK_CANVAS:
    canvas_client = MockCanvasClient()
else:
    # Placeholder for future real Canvas client
    raise NotImplementedError(
        "Real Canvas client not yet implemented. Set USE_MOCK_CANVAS=true")


# Create MCP server instance
server = Server("canvas-ai-assistant")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List all available MCP tools for Canvas interaction.
    """
    return [
        types.Tool(
            name="get_student_courses",
            description="Get all courses for a student by their login/email",
            inputSchema={
                "type": "object",
                "properties": {
                    "login": {
                        "type": "string",
                        "description": "Student login or email address"
                    }
                },
                "required": ["login"]
            }
        ),
        types.Tool(
            name="get_upcoming_assignments",
            description="Get upcoming assignments for a student within specified days",
            inputSchema={
                "type": "object",
                "properties": {
                    "login": {
                        "type": "string",
                        "description": "Student login or email address"
                    },
                    "days": {
                        "type": "number",
                        "description": "Number of days to look ahead (default: 7)",
                        "default": 7
                    }
                },
                "required": ["login"]
            }
        ),
        types.Tool(
            name="get_missing_assignments",
            description="Get missing or overdue assignments for a student",
            inputSchema={
                "type": "object",
                "properties": {
                    "login": {
                        "type": "string",
                        "description": "Student login or email address"
                    }
                },
                "required": ["login"]
            }
        ),
        types.Tool(
            name="get_course_grades",
            description="Get grade summaries for all courses a student is enrolled in",
            inputSchema={
                "type": "object",
                "properties": {
                    "login": {
                        "type": "string",
                        "description": "Student login or email address"
                    }
                },
                "required": ["login"]
            }
        ),
        types.Tool(
            name="get_assignment_grades",
            description="Get individual assignment grades for a student, optionally filtered by course",
            inputSchema={
                "type": "object",
                "properties": {
                    "login": {
                        "type": "string",
                        "description": "Student login or email address"
                    },
                    "course_id": {
                        "type": "string",
                        "description": "Optional course ID to filter grades"
                    }
                },
                "required": ["login"]
            }
        ),
        types.Tool(
            name="get_announcements",
            description="Get recent announcements for all courses a student is enrolled in",
            inputSchema={
                "type": "object",
                "properties": {
                    "login": {
                        "type": "string",
                        "description": "Student login or email address"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of announcements to return (default: 10)",
                        "default": 10
                    }
                },
                "required": ["login"]
            }
        ),
        types.Tool(
            name="get_course_assignments",
            description="Get all assignments for a specific course",
            inputSchema={
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    }
                },
                "required": ["course_id"]
            }
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str,
    arguments: dict[str, Any] | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    """
    if arguments is None:
        arguments = {}

    try:
        if name == "get_student_courses":
            return await get_student_courses(arguments.get("login"))

        elif name == "get_upcoming_assignments":
            return await get_upcoming_assignments(
                arguments.get("login"),
                arguments.get("days", 7)
            )

        elif name == "get_missing_assignments":
            return await get_missing_assignments(arguments.get("login"))

        elif name == "get_course_grades":
            return await get_course_grades(arguments.get("login"))

        elif name == "get_assignment_grades":
            return await get_assignment_grades(
                arguments.get("login"),
                arguments.get("course_id")
            )

        elif name == "get_announcements":
            return await get_announcements(
                arguments.get("login"),
                arguments.get("limit", 10)
            )

        elif name == "get_course_assignments":
            return await get_course_assignments(arguments.get("course_id"))

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error executing tool {name}: {str(e)}"
        )]


# Tool implementation functions

async def get_student_courses(login: str) -> list[types.TextContent]:
    """Get all courses for a student."""
    student = canvas_client.get_student_by_login(login)
    if not student:
        return [types.TextContent(
            type="text",
            text=f"Student not found with login: {login}"
        )]

    courses = canvas_client.get_courses_for_student(student["id"])

    if not courses:
        return [types.TextContent(
            type="text",
            text=f"No courses found for {student['name']}"
        )]

    result = f"Courses for {student['name']} ({login}):\n\n"
    for course in courses:
        result += f"• {course['name']} ({course['code']})\n"
        result += f"  Term: {course['term']}\n"
        result += f"  Course ID: {course['id']}\n\n"

    return [types.TextContent(type="text", text=result)]


async def get_upcoming_assignments(login: str, days: int = 7) -> list[types.TextContent]:
    """Get upcoming assignments for a student."""
    student = canvas_client.get_student_by_login(login)
    if not student:
        return [types.TextContent(
            type="text",
            text=f"Student not found with login: {login}"
        )]

    assignments = canvas_client.get_upcoming_assignments_for_student(
        student["id"],
        within_days=days
    )

    if not assignments:
        return [types.TextContent(
            type="text",
            text=f"No upcoming assignments in the next {days} days for {student['name']}"
        )]

    result = f"Upcoming assignments for {student['name']} (next {days} days):\n\n"
    for assignment in assignments:
        result += f"• {assignment['title']}\n"
        result += f"  Course: {assignment.get('course_name', 'Unknown')} ({assignment.get('course_code', 'N/A')})\n"
        result += f"  Due: {assignment['due_date']}\n"
        result += f"  Points: {assignment.get('points_possible', 'N/A')}\n"
        result += f"  Status: {assignment.get('submission_status', 'not_submitted')}\n"
        if assignment.get('description'):
            result += f"  Description: {assignment['description']}\n"
        result += "\n"

    return [types.TextContent(type="text", text=result)]


async def get_missing_assignments(login: str) -> list[types.TextContent]:
    """Get missing/overdue assignments for a student."""
    student = canvas_client.get_student_by_login(login)
    if not student:
        return [types.TextContent(
            type="text",
            text=f"Student not found with login: {login}"
        )]

    assignments = canvas_client.get_missing_assignments_for_student(
        student["id"])

    if not assignments:
        return [types.TextContent(
            type="text",
            text=f"No missing assignments for {student['name']} - great job staying on top of your work!"
        )]

    result = f"Missing/Overdue assignments for {student['name']}:\n\n"
    for assignment in assignments:
        result += f"• {assignment['title']}\n"
        result += f"  Course: {assignment.get('course_name', 'Unknown')} ({assignment.get('course_code', 'N/A')})\n"
        result += f"  Was due: {assignment['due_date']}\n"
        result += f"  Days overdue: {assignment.get('days_overdue', 'N/A')}\n"
        result += f"  Points: {assignment.get('points_possible', 'N/A')}\n"
        if assignment.get('description'):
            result += f"  Description: {assignment['description']}\n"
        result += "\n"

    return [types.TextContent(type="text", text=result)]


async def get_course_grades(login: str) -> list[types.TextContent]:
    """Get grade summaries for all courses."""
    student = canvas_client.get_student_by_login(login)
    if not student:
        return [types.TextContent(
            type="text",
            text=f"Student not found with login: {login}"
        )]

    grades = canvas_client.get_course_grades_for_student(student["id"])

    if not grades:
        return [types.TextContent(
            type="text",
            text=f"No grade information available for {student['name']}"
        )]

    result = f"Course grades for {student['name']}:\n\n"
    for grade in grades:
        result += f"• {grade.get('course_name', 'Unknown')} ({grade.get('course_code', 'N/A')})\n"
        result += f"  Term: {grade.get('term', 'N/A')}\n"

        if grade.get('current_score') is not None:
            result += f"  Current Score: {grade['current_score']:.1f}%\n"
        else:
            result += f"  Current Score: Not yet available\n"

        if grade.get('letter_grade'):
            result += f"  Letter Grade: {grade['letter_grade']}\n"

        if grade.get('final_score') is not None:
            result += f"  Final Score: {grade['final_score']:.1f}%\n"

        result += "\n"

    return [types.TextContent(type="text", text=result)]


async def get_assignment_grades(
    login: str,
    course_id: Optional[str] = None
) -> list[types.TextContent]:
    """Get individual assignment grades for a student."""
    student = canvas_client.get_student_by_login(login)
    if not student:
        return [types.TextContent(
            type="text",
            text=f"Student not found with login: {login}"
        )]

    grades = canvas_client.get_assignment_grades_for_student(
        student["id"],
        course_id=course_id
    )

    if not grades:
        filter_msg = f" for course {course_id}" if course_id else ""
        return [types.TextContent(
            type="text",
            text=f"No graded assignments found{filter_msg} for {student['name']}"
        )]

    filter_msg = f" for course {course_id}" if course_id else ""
    result = f"Assignment grades{filter_msg} for {student['name']}:\n\n"

    for grade in grades:
        result += f"• {grade.get('assignment_title', 'Unknown Assignment')}\n"
        result += f"  Course: {grade.get('course_name', 'Unknown')} ({grade.get('course_code', 'N/A')})\n"

        if grade.get('score') is not None and grade.get('points_possible'):
            percentage = (float(grade['score']) /
                          float(grade['points_possible'])) * 100
            result += f"  Score: {grade['score']}/{grade['points_possible']} ({percentage:.1f}%)\n"
        elif grade.get('score') is not None:
            result += f"  Score: {grade['score']}\n"

        if grade.get('grade'):
            result += f"  Grade: {grade['grade']}\n"

        if grade.get('feedback'):
            result += f"  Feedback: {grade['feedback']}\n"

        if grade.get('graded_at'):
            result += f"  Graded: {grade['graded_at']}\n"

        result += "\n"

    return [types.TextContent(type="text", text=result)]


async def get_announcements(login: str, limit: int = 10) -> list[types.TextContent]:
    """Get recent announcements for a student's courses."""
    student = canvas_client.get_student_by_login(login)
    if not student:
        return [types.TextContent(
            type="text",
            text=f"Student not found with login: {login}"
        )]

    announcements = canvas_client.get_announcements_for_student(
        student["id"],
        limit=limit
    )

    if not announcements:
        return [types.TextContent(
            type="text",
            text=f"No recent announcements for {student['name']}"
        )]

    result = f"Recent announcements for {student['name']}:\n\n"
    for announcement in announcements:
        result += f"• {announcement['title']}\n"
        result += f"  Course: {announcement.get('course_name', 'Unknown')} ({announcement.get('course_code', 'N/A')})\n"
        result += f"  Posted: {announcement['posted_date']}\n"
        if announcement.get('content'):
            result += f"  {announcement['content']}\n"
        result += "\n"

    return [types.TextContent(type="text", text=result)]


async def get_course_assignments(course_id: str) -> list[types.TextContent]:
    """Get all assignments for a specific course."""
    course = canvas_client.get_course_by_id(course_id)
    if not course:
        return [types.TextContent(
            type="text",
            text=f"Course not found with ID: {course_id}"
        )]

    assignments = canvas_client.get_assignments_for_course(course_id)

    if not assignments:
        return [types.TextContent(
            type="text",
            text=f"No assignments found for {course['name']}"
        )]

    result = f"Assignments for {course['name']} ({course['code']}):\n\n"
    for assignment in assignments:
        result += f"• {assignment['title']}\n"
        if assignment.get('due_date'):
            result += f"  Due: {assignment['due_date']}\n"
        result += f"  Points: {assignment.get('points_possible', 'N/A')}\n"
        result += f"  Status: {assignment.get('status', 'N/A')}\n"
        if assignment.get('description'):
            result += f"  Description: {assignment['description']}\n"
        result += "\n"

    return [types.TextContent(type="text", text=result)]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="canvas-ai-assistant",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
