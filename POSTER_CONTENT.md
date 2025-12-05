# Canvas AI Assistant - MCP Server
## Poster Content for Missing Sections

---

## SYSTEM DESIGN

### Four-Layer Architecture

**1. Data Ingestion Layer**
- Canvas API client with secure token authentication
- Scheduled synchronization jobs (periodic data refresh)
- Data transformation and validation pipeline
- Rate limiting and error recovery mechanisms

**2. Backend Server & Database (MCP Server)**
- Model Context Protocol (MCP) server implementation
- PostgreSQL database with SQLAlchemy ORM
- 7 MCP tools for Canvas data interaction
- RESTful API endpoints for client applications

**3. AI Core Layer (LLM Integration)**
- Query processing with intent extraction
- Context retrieval using RAG pattern
- LLM integration (Claude via MCP protocol)
- Natural language response generation

**4. Client & Integration Layer**
- Claude Desktop chat interface
- Google Calendar automation (planned)
- Notification system for deadlines
- LTI app for Canvas integration (stretch goal)

### Data Flow
```
Canvas LMS → API Sync → PostgreSQL → MCP Tools → Claude AI → User
                ↓
         Google Calendar
```

---

## OBJECT DESIGN

### Database Schema

**Core Models (SQLAlchemy ORM):**

**Course Model**
- Primary Key: Canvas course ID
- Attributes: name, code, term
- Relationships: assignments, announcements, grades
- Validation: name required, length constraints

**Assignment Model**
- Primary Key: Canvas assignment ID
- Foreign Key: course_id
- Attributes: title, description, due_date, points_possible, status
- Status Enum: not_started, in_progress, completed, overdue, graded
- Methods: is_overdue property, validate()

**Announcement Model**
- Primary Key: Canvas announcement ID
- Foreign Key: course_id
- Attributes: title, content, posted_date
- Relationships: linked to course

**Grade Model**
- Primary Key: auto-increment ID
- Foreign Keys: course_id, assignment_id
- Attributes: score, grade, feedback, graded_at
- Relationships: course and assignment references

### MCP Tools Architecture

**7 MCP Tools Implemented:**
1. `get_student_courses` - Retrieve enrolled courses
2. `get_upcoming_assignments` - Filter by date range
3. `get_missing_assignments` - Identify overdue work
4. `get_course_grades` - Overall grade summaries
5. `get_assignment_grades` - Individual assignment scores
6. `get_announcements` - Recent course updates
7. `get_course_assignments` - All assignments per course

**Tool Pattern:**
- Input validation with JSON schema
- Async execution for performance
- Structured text responses
- Error handling with descriptive messages

---

## VERIFICATION

### Testing Strategy

**1. Unit Testing**
- Mock Canvas client with realistic test data
- Component isolation with pytest framework
- 80%+ code coverage target for core logic
- Automated test suite (`test_mock_client.py`)

**2. Integration Testing**
- MCP tool testing with Claude Desktop
- Database CRUD operations validation
- End-to-end query processing workflows
- Mock data includes 2 students, 3 courses, 7 assignments

**3. Mock Data Validation**
- High-fidelity Canvas data simulation
- Multiple assignment states (completed, overdue, upcoming)
- Realistic grade distributions and feedback
- Test logins: alex@example.edu, jordan@example.edu

**4. System Verification**
- Database health checks and connectivity tests
- MCP server connection validation
- Query response time monitoring (<2s target)
- Error handling and recovery testing

**5. Security Testing**
- Input validation and sanitization
- SQL injection prevention
- Secure token management
- Data encryption verification

### Test Results
✓ All 8 MockCanvasClient methods validated
✓ MCP tools functional with Claude Desktop
✓ Database models with validation constraints
✓ Automated setup and health check scripts

---

## ACKNOWLEDGEMENT

This senior design project is based upon the work supported by:

**Mentor:** Masoud Sadjadi, Florida International University

**Key Technologies:**
- Model Context Protocol (MCP) by Anthropic
- Canvas LMS API by Instructure
- Claude AI by Anthropic
- PostgreSQL and SQLAlchemy ORM
- Python asyncio and MCP SDK

**Special Thanks:**
- FIU School of Computing and Information Sciences
- Canvas LMS development team for API documentation
- Anthropic for MCP protocol specification
- Open source community for Python libraries

---

## REFERENCES

1. **Canvas LMS API Documentation**
   - Instructure Canvas REST API Reference
   - https://canvas.instructure.com/doc/api/

2. **Model Context Protocol (MCP)**
   - Anthropic MCP Specification
   - https://modelcontextprotocol.io/

3. **Anthropic Claude Documentation**
   - Claude Desktop Integration Guide
   - https://docs.anthropic.com/

4. **SQLAlchemy ORM**
   - Database Toolkit for Python
   - https://www.sqlalchemy.org/

5. **PostgreSQL Database**
   - Advanced Open Source Database
   - https://www.postgresql.org/

6. **Python asyncio**
   - Asynchronous I/O Framework
   - https://docs.python.org/3/library/asyncio.html

7. **RAG Pattern Research**
   - Retrieval-Augmented Generation for LLMs
   - Lewis et al., 2020

8. **FIU Senior Design Program**
   - School of Computing and Information Sciences
   - Florida International University

---

## SUMMARY STATISTICS

**Project Metrics:**
- 4-layer modular architecture
- 7 MCP tools implemented
- 4 database models with relationships
- 2 mock students with realistic data
- 3 courses across different subjects
- 7 assignments with various states
- 100% mock client test coverage
- PostgreSQL with migration system
- Python 3.8+ with asyncio
- MCP protocol integration

**Development Status:**
- ✅ Phase 1: Foundation & Mock Implementation (Complete)
- 🔄 Phase 2: Database Integration (In Progress)
- 📋 Phase 3: Real Canvas API & Deployment (Planned)
