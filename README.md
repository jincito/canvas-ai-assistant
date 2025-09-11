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

4. **Run the conceptual server:**

   ```bash
   python mcp_server/app.py
   ```

   The server will start on `http://127.0.0.1:5000`.

5. **Test the API:**
   Use a tool like Postman to send a `POST` request to `http://127.0.0.1:5000/api/ask` with a JSON body:

   ```json
   {
     "question": "what do I have for my project in CIS4951?"
   }
   ```

## ⌨️ Example

```bash
curl -X POST <http://127.0.0.1:5000/api/ask> \
       -H "Content-Type: application/json" \
       -d '{"question": "what do I have for my project in CIS4951?"}'
```

**Response:**

```json
{
  "answer": "Based on your Canvas data, here's what I found:\n\n\u2022 Assignment: Senior Project Proposal for CIS4951 - Due: 2024-02-15 - Status: completed\n\u2022 Assignment: Project Implementation Phase 1 for CIS4951 - Due: 2024-03-15 - Status: in_progress\n\nFor your CIS4951 senior project, you have both a completed proposal and an ongoing implementation phase.",
  "question": "what do I have for my project in CIS4951?",
  "timestamp": "2025-09-10T21:35:57.704856"
}
```

---

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

---

## 📄 License
