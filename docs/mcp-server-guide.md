# Canvas AI Assistant MCP Server Guide

## Overview

The Canvas AI Assistant MCP Server provides a Model Context Protocol (MCP) interface for AI assistants like Claude Desktop to interact with Canvas LMS data. Due to Canvas security policies that prevent students from creating additional API tokens, this implementation uses a high-fidelity mock Canvas client for development and testing.

## Architecture

### Components

1. **MockCanvasClient** (`mcp_server/mock_canvas_client.py`)
   - Loads realistic Canvas data from JSON
   - Provides methods for querying courses, assignments, grades, and announcements
   - Implements the same interface as the future RealCanvasClient

2. **MCP Server** (`mcp_server/mcp_app.py`)
   - Implements the Model Context Protocol
   - Exposes 7 tools for Canvas interaction
   - Uses MockCanvasClient by default (configurable via environment variable)

3. **Mock Data** (`mock_data/canvas_data.json`)
   - Realistic Canvas data structure
   - 2 students, 3 courses, 7 assignments
   - Includes submissions, grades, and announcements

## Available MCP Tools

### 1. get_student_courses
Get all courses for a student by their login/email.

**Parameters:**
- `login` (string, required): Student login or email address

**Example:**
```
What courses am I enrolled in? (login: alex@example.edu)
```

### 2. get_upcoming_assignments
Get upcoming assignments for a student within specified days.

**Parameters:**
- `login` (string, required): Student login or email address
- `days` (number, optional): Number of days to look ahead (default: 7)

**Example:**
```
What assignments are due in the next 2 weeks? (login: alex@example.edu, days: 14)
```

### 3. get_missing_assignments
Get missing or overdue assignments for a student.

**Parameters:**
- `login` (string, required): Student login or email address

**Example:**
```
Do I have any missing assignments? (login: alex@example.edu)
```

### 4. get_course_grades
Get grade summaries for all courses a student is enrolled in.

**Parameters:**
- `login` (string, required): Student login or email address

**Example:**
```
What are my current grades? (login: alex@example.edu)
```

### 5. get_assignment_grades
Get individual assignment grades for a student, optionally filtered by course.

**Parameters:**
- `login` (string, required): Student login or email address
- `course_id` (string, optional): Course ID to filter grades

**Example:**
```
Show me my graded assignments (login: alex@example.edu)
```

### 6. get_announcements
Get recent announcements for all courses a student is enrolled in.

**Parameters:**
- `login` (string, required): Student login or email address
- `limit` (number, optional): Maximum number of announcements (default: 10)

**Example:**
```
What are the latest announcements? (login: alex@example.edu)
```

### 7. get_course_assignments
Get all assignments for a specific course.

**Parameters:**
- `course_id` (string, required): Course ID

**Example:**
```
Show me all assignments for course c101
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Claude Desktop or another MCP-compatible client

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test the mock client:**
   ```bash
   python3 test_mock_client.py
   ```

   This will verify that all MockCanvasClient methods work correctly.

### Configuring Claude Desktop

1. **Locate your Claude Desktop configuration file:**
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. **Add the MCP server configuration:**
   ```json
   {
     "mcpServers": {
       "canvas-ai-assistant": {
         "command": "python3",
         "args": [
           "/absolute/path/to/canvas-ai-assistant/run_mcp_server.py"
         ],
         "env": {
           "USE_MOCK_CANVAS": "true"
         }
       }
     }
   }
   ```

   **Important:** Replace `/absolute/path/to/canvas-ai-assistant` with the actual absolute path to your project directory.

3. **Restart Claude Desktop** to load the new MCP server.

4. **Verify the connection:**
   - Open Claude Desktop
   - Look for the MCP server indicator (usually a plug icon or similar)
   - The server should show as connected

### Testing with Claude Desktop

Once configured, you can ask Claude questions like:

- "What courses am I enrolled in?" (use login: alex@example.edu)
- "What assignments are due in the next week?"
- "Do I have any missing assignments?"
- "What are my current grades in all courses?"
- "Show me recent announcements"

**Note:** When testing, use one of the mock student logins:
- `alex@example.edu` (enrolled in 3 courses)
- `jordan@example.edu` (enrolled in 2 courses)

## Mock Data Details

### Students

1. **Alex Rivera** (`alex@example.edu`)
   - Enrolled in 3 courses
   - Has completed, in-progress, and upcoming assignments
   - Has 1 missing assignment
   - Has grades in one course

2. **Jordan Smith** (`jordan@example.edu`)
   - Enrolled in 2 courses
   - Similar assignment and grade structure

### Courses

1. **CIS4951** - Introduction to Artificial Intelligence
   - 3 assignments (proposal, implementation, demo)
   - Fall 2024 term

2. **CSCI5707** - Advanced Database Systems
   - 2 assignments (design, optimization)
   - Fall 2024 term

3. **CSCI5801** - Software Engineering Capstone
   - 2 sprint deliverables
   - Fall 2024 term

### Assignment States

The mock data includes assignments in various states:
- **Completed**: Submitted and graded
- **In Progress**: Currently being worked on
- **Not Started**: Future assignments
- **Overdue**: Past due date without submission

## Configuration Options

### Environment Variables

- `USE_MOCK_CANVAS` (default: `true`)
  - Set to `true` to use MockCanvasClient
  - Set to `false` to use RealCanvasClient (not yet implemented)

### Mock Data Location

The mock data is loaded from `mock_data/canvas_data.json`. You can modify this file to:
- Add more students, courses, or assignments
- Change due dates
- Update grades and submissions
- Add more announcements

After modifying the mock data, restart the MCP server for changes to take effect.

## Troubleshooting

### MCP Server Not Connecting

1. **Check the path:** Ensure the absolute path in your Claude Desktop config is correct
2. **Check Python:** Verify `python3` is available in your PATH
3. **Check dependencies:** Run `pip install -r requirements.txt` again
4. **Check logs:** Look for error messages in Claude Desktop's developer console

### "Student not found" Errors

- Make sure you're using a valid mock student login:
  - `alex@example.edu`
  - `jordan@example.edu`
- Check that the mock data file exists at `mock_data/canvas_data.json`

### No Upcoming Assignments

- Check the due dates in `mock_data/canvas_data.json`
- Ensure dates are in the future relative to the current date
- The mock data uses dates in November-December 2025

### Import Errors

- Ensure you're running from the project root directory
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check that the virtual environment is activated (if using one)

## Development

### Adding New Tools

To add a new MCP tool:

1. Add the tool definition in `handle_list_tools()` in `mcp_server/mcp_app.py`
2. Add the tool handler in `handle_call_tool()`
3. Implement the tool function (e.g., `async def get_new_feature(...)`)
4. Add corresponding method to `MockCanvasClient` if needed

### Switching to Real Canvas API

When ready to use the real Canvas API:

1. Implement `RealCanvasClient` in `mcp_server/real_canvas_client.py`
2. Set `USE_MOCK_CANVAS=false` in your environment
3. Configure Canvas API credentials in `.env`:
   ```
   CANVAS_API_URL=https://your-institution.instructure.com
   CANVAS_API_TOKEN=your_token_here
   ```

## Future Enhancements

- Database integration for persistent storage
- Real Canvas API client implementation
- Additional tools for submitting assignments
- Calendar integration for due date reminders
- Notification system for new announcements
- LTI app for direct Canvas integration

## Support

For issues or questions:
1. Check this guide and the main README.md
2. Review the code comments in `mcp_server/mock_canvas_client.py`
3. Run the test script: `python3 test_mock_client.py`
4. Check the project's issue tracker on GitHub
