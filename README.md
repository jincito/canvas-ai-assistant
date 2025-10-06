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
2. **Backend Server & Database (MCP Server)**: A Python server (using Flask or FastAPI) stores the synced data in a database (like PostgreSQL). It exposes a secure REST API for clients to use, including a main `/ask` endpoint for LLM interaction.
3. **LLM & Logic Layer (AI Core)**: Implements a Retrieval-Augmented Generation (RAG) pattern. When a user asks a question, the backend retrieves relevant data from its database and provides it as context to an LLM (like Gemini or Claude) to generate a human-readable answer.
4. **Client & Integration Layer**: This includes a primary chat client, automation hooks for services like Google Calendar, and notification systems. A stretch goal is to build an LTI app for direct integration into the Canvas UI.

---

## 🚀 Getting Started

**Prerequisites:**

- Python 3.8+
- pip
- A tool to make API requests (like Postman or curl)

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

5. **Run the development server:**

   ```bash
   python mcp_server/app.py
   ```

   The server will start on `http://127.0.0.1:5000`.

6. **Test the API:**
   Use a tool like Postman to send a `POST` request to `http://127.0.0.1:5000/api/ask` with a JSON body:

   ```json
   {
     "question": "what do I have for my project in CIS4951?"
   }
   ```

## 📋 Current Implementation Status

The project is currently in **Phase 1: Foundation & Database Infrastructure** with a working Flask server that provides:

- ✅ **Mock Data System**: Simulated Canvas data for development and testing
- ✅ **Basic RAG Pattern**: Query processing with context retrieval and response generation
- ✅ **REST API Endpoints**: `/api/ask`, `/api/health`, and `/api/data`
- ✅ **Flask Application**: Development server with JSON request/response handling
- ✅ **Database Models**: Complete SQLAlchemy models for courses, assignments, announcements, and grades
- ✅ **Database Infrastructure**: Connection management, configuration, and migration system
- ✅ **Database Setup Tools**: Automated database initialization and management scripts
- 🔄 **Canvas API Integration**: Placeholder implementation in `scripts/canvas_sync.py`
- 🔄 **Database Integration**: Connecting Flask API to PostgreSQL database
- 🔄 **LLM Integration**: Template-based responses (LLM service integration planned)

For detailed development status and progress tracking, see [docs/development-status.md](docs/development-status.md).

## 📚 API Documentation

### Available Endpoints

#### POST `/api/ask`
Main endpoint for natural language queries about Canvas data.

**Request:**
```json
{
  "question": "what do I have for my project in CIS4951?"
}
```

**Response:**
```json
{
  "answer": "Based on your Canvas data, here's what I found:\n\n• Assignment: Senior Project Proposal for CIS4951 - Due: 2024-02-15 - Status: completed\n• Assignment: Project Implementation Phase 1 for CIS4951 - Due: 2024-03-15 - Status: in_progress\n\nFor your CIS4951 senior project, you have both a completed proposal and an ongoing implementation phase.",
  "question": "what do I have for my project in CIS4951?",
  "timestamp": "2025-09-10T21:35:57.704856"
}
```

#### GET `/api/health`
Health check endpoint for monitoring server status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-10T21:35:57.704856"
}
```

#### GET `/api/data`
Retrieve all available Canvas data (currently mock data).

**Response:**
```json
{
  "assignments": [...],
  "announcements": [...],
  "grades": [...]
}
```

### Example Usage

```bash
# Ask a question about assignments
curl -X POST http://127.0.0.1:5000/api/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "what assignments do I have due this week?"}'

# Check server health
curl http://127.0.0.1:5000/api/health

# Get all data
curl http://127.0.0.1:5000/api/data
```

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
