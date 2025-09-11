from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

mock_data = {
    "assignments": [
        {
            "id": 1,
            "course": "CIS4951",
            "title": "Senior Project Proposal",
            "due_date": "2024-02-15",
            "description": "Submit a detailed proposal for your senior capstone project",
            "status": "completed"
        },
        {
            "id": 2,
            "course": "CIS4951", 
            "title": "Project Implementation Phase 1",
            "due_date": "2024-03-15",
            "description": "Complete the first implementation milestone of your project",
            "status": "in_progress"
        }
    ],
    "announcements": [
        {
            "id": 1,
            "course": "CIS4951",
            "title": "Project Demo Day Scheduled",
            "content": "The final project demonstrations will be held on April 20th",
            "posted_date": "2024-02-01"
        }
    ],
    "grades": [
        {
            "course": "CIS4951",
            "assignment": "Senior Project Proposal",
            "grade": "95/100",
            "feedback": "Excellent proposal with clear objectives"
        }
    ]
}

def search_relevant_data(question):
    question_lower = question.lower()
    relevant_items = []
    
    if "assignment" in question_lower or "project" in question_lower or "due" in question_lower:
        for assignment in mock_data["assignments"]:
            if any(keyword in assignment["course"].lower() or 
                   keyword in assignment["title"].lower() or 
                   keyword in assignment["description"].lower() 
                   for keyword in question_lower.split()):
                relevant_items.append(f"Assignment: {assignment['title']} for {assignment['course']} - Due: {assignment['due_date']} - Status: {assignment['status']}")
    
    if "announcement" in question_lower or "news" in question_lower:
        for announcement in mock_data["announcements"]:
            if any(keyword in announcement["course"].lower() or 
                   keyword in announcement["title"].lower() or 
                   keyword in announcement["content"].lower() 
                   for keyword in question_lower.split()):
                relevant_items.append(f"Announcement: {announcement['title']} - {announcement['content']}")
    
    if "grade" in question_lower or "score" in question_lower:
        for grade in mock_data["grades"]:
            if any(keyword in grade["course"].lower() or 
                   keyword in grade["assignment"].lower() 
                   for keyword in question_lower.split()):
                relevant_items.append(f"Grade: {grade['assignment']} - {grade['grade']} - {grade['feedback']}")
    
    return relevant_items

def generate_llm_response(question, context):
    if not context:
        return "I couldn't find any relevant information in your Canvas data for that question."
    
    response = f"Based on your Canvas data, here's what I found:\n\n"
    for item in context:
        response += f"• {item}\n"
    
    if "project" in question.lower() and "cis4951" in question.lower():
        response += "\nFor your CIS4951 senior project, you have both a completed proposal and an ongoing implementation phase."
    
    return response

@app.route('/api/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({"error": "No question provided"}), 400
        
        context = search_relevant_data(question)
        answer = generate_llm_response(question, context)
        
        return jsonify({
            "question": question,
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/data', methods=['GET'])
def get_all_data():
    return jsonify(mock_data)

if __name__ == '__main__':
    print("Starting Canvas AI Assistant MCP Server...")
    print("Server will be available at: http://127.0.0.1:5000")
    print("Test the /api/ask endpoint with a POST request")
    app.run(debug=True, host='127.0.0.1', port=5000)