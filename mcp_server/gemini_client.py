import os
import requests
import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool
from dotenv import load_dotenv

load_dotenv() 

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in .env file.")
    exit(1)

genai.configure(api_key=api_key)

MCP_SERVER_URL = "http://127.0.0.1:8000/api/data" 

def get_canvas_data():
    """
    Fetches the student's latest academic data from the local MCP server.
    Returns:
        dict: A JSON object containing courses, assignments, and grades.
    """
    print(f"\n[Client] Calling MCP Server at {MCP_SERVER_URL}...")
    try:
        response = requests.get(MCP_SERVER_URL)
        response.raise_for_status()
        data = response.json()
        print("[Client] ✅ Received data from server.")
        return data
    except Exception as e:
        print(f"[Client] Error connecting to server: {e}")
        return {"error": "Could not connect to MCP server. Is it running?"}

canvas_tool = Tool(
    function_declarations=[
        FunctionDeclaration(
            name="get_canvas_data",
            description="Retrieve current academic data including courses, assignments, and grades from Canvas.",
        )
    ]
)

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=[canvas_tool] 
)

def start_chat():
    chat = model.start_chat(enable_automatic_function_calling=True)
    
    print("------------------------------------------------------")
    print(" Canvas AI Assistant (Gemini Client) Ready!")
    print("   Type 'quit' to exit.")
    print("------------------------------------------------------")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']:
            break

        try:
            response = chat.send_message(user_input)
            
            response_text = ""
            for part in response.candidates[0].content.parts:
                if part.text:
                    response_text += part.text
                elif part.function_call:
                    response_text += f" (Gemini requested tool: {part.function_call.name})"
            
            print(f"Gemini: {response_text}")
            
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    start_chat()