# Canvas AI Assistant

## 📖 Project Overview

**Goal:** To develop a secure backend service (the "MCP Server") that syncs with a student's Canvas LMS data. This service will provide an API that allows various clients, such as a desktop AI chat application and automation services (like Google Calendar), to access and interact with the student's academic information in a conversational manner using a Large Language Model (LLM).

**Core Problem:** Students often have to manually check multiple pages within Canvas to keep track of announcements, assignments, and events. This project aims to centralize that information and make it accessible through natural language queries and automated notifications.

---

## 👥 Project Team

| Name                |
| ------------------- |
| Edgar Velarde       |
| Alberto Abrahantes  |
| Jin Carballosa      |
| Nitin Chokkalla     |
| Sebastian Rodriguez |

---

## ⚙️ System Architecture

The project is broken down into four main components:

1. **Data Ingestion Layer**: A scheduled job uses the official Canvas API to periodically pull student data (assignments, announcements, grades, etc.).
2. **Backend Server & Database (MCP Server)**: A Python MCP server stores the synced data in a database (like PostgreSQL). It exposes tools through the Model Context Protocol for AI assistants like Claude to interact with Canvas data.
3. **LLM & Logic Layer (AI Core)**: AI assistants like Claude use the MCP tools to retrieve relevant Canvas data and generate human-readable responses to student queries.
4. **Client & Integration Layer**: This includes a primary chat client, automation hooks for services like Google Calendar, and notification systems. A stretch goal is to build an LTI app for direct integration into the Canvas UI.

---

## 🚀 Getting Started

> **Quick Start:** See [QUICKSTART.md](QUICKSTART.md) for a 5-minute setup guide!

**Prerequisites:**

- Python 3.8+
- pip
- (Optional) PostgreSQL for database development
- (Optional) Claude Desktop or another MCP-compatible client

**Installation & Setup:**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/canvas-ai-assistant.git
   cd canvas-ai-assistant
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database (optional):**

   For database development, you can set up PostgreSQL:
   
   ```bash
   # Initialize database and apply migrations
   python scripts/db_setup.py setup
   
   # Check database connectivity
   python scripts/db_setup.py health
   ```

### Running the MCP Server (Recommended)

The MCP server provides a standardized interface for AI assistants like Claude Desktop to interact with Canvas data.

1. **Run the MCP server:**

   ```bash
   python run_mcp_server.py
   ```

2. **Configure Claude Desktop (or another MCP client):**

   Add the following to your Claude Desktop MCP configuration file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

   ```json
   {
     "mcpServers": {
       "canvas-ai-assistant": {
         "command": "python",
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

   Replace `/absolute/path/to/canvas-ai-assistant` with the actual path to your project directory.

3. **Restart Claude Desktop** to load the new MCP server.

4. **Test the MCP tools** by asking Claude questions like:
   - "What courses am I enrolled in?" (use login: alex@example.edu)
   - "What assignments are due soon?"
   - "Do I have any missing assignments?"
   - "What are my current grades?"



## 📋 Current Implementation Status

The project is currently in **Phase 1: Foundation & Mock Implementation** with a fully functional MCP server:

- ✅ **Mock Canvas Client**: High-fidelity mock implementation of Canvas API with realistic data
- ✅ **MCP Server**: Full Model Context Protocol server with 7 tools for Canvas interaction
- ✅ **Mock Data System**: Comprehensive simulated Canvas data (students, courses, assignments, grades, announcements)
- ✅ **Basic RAG Pattern**: Query processing with context retrieval and response generation
- ✅ **Database Models**: Complete SQLAlchemy models for courses, assignments, announcements, and grades
- ✅ **Database Infrastructure**: Connection management, configuration, and migration system
- ✅ **Database Setup Tools**: Automated database initialization and management scripts
- 🔄 **Canvas API Integration**: Placeholder implementation in `scripts/canvas_sync.py`
- 🔄 **Database Integration**: Connecting API to PostgreSQL database
- 🔄 **LLM Integration**: Template-based responses (LLM service integration planned)

### MCP Tools Available

The MCP server provides the following tools for AI assistants:

1. **get_student_courses** - Get all courses for a student
2. **get_upcoming_assignments** - Get assignments due within specified days
3. **get_missing_assignments** - Get overdue/missing assignments
4. **get_course_grades** - Get grade summaries for all courses
5. **get_assignment_grades** - Get individual assignment grades
6. **get_announcements** - Get recent course announcements
7. **get_course_assignments** - Get all assignments for a specific course

For detailed development status and progress tracking, see [docs/development-status.md](docs/development-status.md).

For complete MCP server documentation, see [docs/mcp-server-guide.md](docs/mcp-server-guide.md).

## 🎭 Mock Canvas Data

Due to Canvas security policies preventing students from creating additional API tokens, this project uses a high-fidelity mock Canvas client for development and testing.

### Mock Data Structure

The mock data (`mock_data/canvas_data.json`) includes:

- **Students**: 2 sample students with realistic profiles
  - Alex Rivera (alex@example.edu) - enrolled in 3 courses
  - Jordan Smith (jordan@example.edu) - enrolled in 2 courses

- **Courses**: 3 courses across different subjects
  - CIS4951: Introduction to Artificial Intelligence
  - CSCI5707: Advanced Database Systems
  - CSCI5801: Software Engineering Capstone

- **Assignments**: 7 assignments with various statuses
  - Completed, in progress, not started, and overdue assignments
  - Realistic due dates, points, and descriptions

- **Submissions & Grades**: Assignment submissions with grading information
- **Announcements**: Course announcements with realistic content
- **Course Grades**: Overall grade summaries per course

### Using Mock Data

The mock client is enabled by default via the `USE_MOCK_CANVAS` environment variable. To test with the mock data:

1. Use login `alex@example.edu` or `jordan@example.edu` when querying student information
2. The mock client provides realistic responses for all Canvas operations
3. Data includes various assignment states (upcoming, missing, graded) for comprehensive testing

### Switching to Real Canvas API

When ready to connect to the real Canvas API:

1. Set `USE_MOCK_CANVAS=false` in your environment
2. Implement the `RealCanvasClient` class (currently a placeholder)
3. Configure Canvas API credentials in `.env`



## 🗄️ Database Infrastructure

The project includes a complete database layer built with SQLAlchemy and PostgreSQL:

### Database Models
- **Course**: Canvas course information (id, name, code, term)
- **Assignment**: Assignment details with due dates and status tracking
- **Announcement**: Course announcements and news
- **Grade**: Grade records with scores and feedback

### Database Management
The `scripts/db_setup.py` script provides database management commands:

```bash
# Set up database with initial schema
python scripts/db_setup.py setup

# Check database connectivity and health
python scripts/db_setup.py health

# Reset database (drop and recreate all tables)
python scripts/db_setup.py reset
```

### Configuration
Database configuration is managed through environment variables:
- `DB_HOST`: Database host (default: localhost)
- `DB_PORT`: Database port (default: 5432)
- `DB_NAME`: Database name (default: canvas_ai_assistant)
- `DB_USER`: Database username (default: postgres)
- `DB_PASSWORD`: Database password
- `DB_POOL_SIZE`: Connection pool size (default: 5)

### Migration System
The project includes a migration management system for database schema changes:
- Version-controlled migrations in `mcp_server/migrations/versions/`
- Automatic migration tracking and application
- Rollback capabilities for schema changes

---

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

---

## 📄 License
