# Canvas AI Assistant Architecture

## System Overview

The Canvas AI Assistant is designed as a modular system with four main layers:

### 1. Data Ingestion Layer
- **Purpose**: Fetch and synchronize data from Canvas LMS
- **Components**:
  - Canvas API client (`scripts/canvas_sync.py`)
  - Scheduled job runner
  - Data validation and transformation

### 2. Backend Server & Database (MCP Server)
- **Purpose**: Store synced data and provide MCP tools for AI assistants
- **Components**:
  - MCP server (`mcp_server/mcp_app.py`)
  - PostgreSQL database
  - Model Context Protocol tools
  - Authentication and authorization

### 3. LLM & Logic Layer (AI Core)
- **Purpose**: Process natural language queries using RAG pattern
- **Components**:
  - Query processing engine
  - Context retrieval system
  - LLM integration (Gemini/Claude)
  - Response generation

### 4. Client & Integration Layer
- **Purpose**: Provide user interfaces and integrations
- **Components**:
  - Chat client application
  - Google Calendar integration
  - Notification system
  - LTI app (stretch goal)

## Data Flow

1. **Sync Process**: Canvas API → Data Ingestion → Database
2. **Query Process**: User Question → Context Retrieval → LLM → Response
3. **Integration Process**: Scheduled Events → External Services

## Database Architecture

### Data Models
The system uses SQLAlchemy ORM with the following core models:

- **Course**: Canvas course information with relationships to assignments, announcements, and grades
- **Assignment**: Assignment details with due dates, status tracking, and grade relationships
- **Announcement**: Course announcements with content and posting dates
- **Grade**: Grade records linking courses and assignments with scores and feedback

### Database Management
- **Configuration**: Environment-based configuration with connection pooling
- **Migrations**: Version-controlled schema changes with rollback capabilities
- **Health Monitoring**: Connection status and performance monitoring
- **Session Management**: Automatic session cleanup and transaction handling

## Security Considerations

- API token management
- Data encryption at rest and in transit
- User authentication and authorization
- Rate limiting and API quotas

## Technology Stack

- **Backend**: Python 3.8+, MCP (Model Context Protocol) server
- **Database**: PostgreSQL with SQLAlchemy ORM (models implemented, integration in progress)
- **LLM**: Anthropic Claude via MCP protocol
- **Development**: Virtual environment, pip package management
- **Version Control**: Git with clean .gitignore for IDE and personal configurations
- **Deployment**: Docker, Cloud hosting (planned)
- **Integration**: Canvas API (placeholder), Google Calendar API (planned)

## Current Implementation Status

### ✅ Completed Components
- **MCP Server**: Full Model Context Protocol implementation with 7 tools
- **Mock Canvas Client**: High-fidelity mock implementation of Canvas API
- **Mock Data System**: Comprehensive simulated Canvas data structure for development
- **Development Environment**: Virtual environment setup with requirements.txt
- **Database Models**: Complete SQLAlchemy models for courses, assignments, announcements, and grades
- **Database Infrastructure**: Connection management, configuration, and migration system
- **Database Setup Tools**: Automated database initialization and management scripts

### 🔄 In Progress Components
- **Database Integration**: Connecting MCP tools to PostgreSQL database
- **Real Canvas API Client**: Authentication and data synchronization
- **Authentication System**: Secure token management
- **Error Handling**: Comprehensive error responses and logging

### 📋 Planned Components
- **Google Calendar Integration**: Assignment due date synchronization
- **LTI Application**: Direct Canvas integration
- **Docker Deployment**: Containerized application setup
- **Comprehensive Testing**: Unit and integration test coverage
- **Monitoring & Logging**: Performance metrics and structured logging
## Current
 Mock Data Structure

The application currently uses mock data to simulate Canvas LMS data structure for development and testing:

### Assignments
```json
{
  "id": 1,
  "course": "CIS4951",
  "title": "Senior Project Proposal",
  "due_date": "2024-02-15",
  "description": "Submit a detailed proposal for your senior capstone project",
  "status": "completed"
}
```

### Announcements
```json
{
  "id": 1,
  "course": "CIS4951",
  "title": "Project Demo Day Scheduled",
  "content": "The final project demonstrations will be held on April 20th",
  "posted_date": "2024-02-01"
}
```

### Grades
```json
{
  "course": "CIS4951",
  "assignment": "Senior Project Proposal",
  "grade": "95/100",
  "feedback": "Excellent proposal with clear objectives"
}
```

This mock data structure will be replaced with actual Canvas API data once the synchronization component is implemented.