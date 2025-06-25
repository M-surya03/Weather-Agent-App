from flask import Flask, render_template, request, jsonify
import os
import sys
import json
import asyncio
import logging
import contextlib
import threading
from datetime import datetime

from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# --- Flask App Setup ---
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')

# --- Constants ---
APP_NAME = "weather_agent_app"
MODEL_NAME = "gemini-2.0-flash"

# --- Weather Agent ---
agent = LlmAgent(
    model=MODEL_NAME,
    name="weather_agent",
    description="Provides weather updates based on user queries.",
    instruction="""
You are a helpful weather assistant. When a user asks for the weather in a specific city, respond directly using your own knowledge. 
Provide current weather conditions, temperature, and any relevant weather information. Keep responses conversational and helpful.
""",
)

# --- Runner Setup ---
session_service = InMemorySessionService()
runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)

# --- Initialize session service ---
def init_session_service():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        session_service.create_session(
            app_name=APP_NAME, 
            user_id="web_user", 
            session_id="web_session"
        )
    )
    loop.close()

# Initialize session in a separate thread
init_thread = threading.Thread(target=init_session_service)
init_thread.start()
init_thread.join()

# --- Suppress stdout/stderr ---
@contextlib.contextmanager
def suppress_stdout_stderr():
    old_stdout_fd = os.dup(1)
    old_stderr_fd = os.dup(2)
    with open(os.devnull, 'w') as devnull:
        os.dup2(devnull.fileno(), 1)
        os.dup2(devnull.fileno(), 2)
        try:
            yield
        finally:
            os.dup2(old_stdout_fd, 1)
            os.dup2(old_stderr_fd, 2)

# --- Ask the Agent Function ---
def ask_agent(query: str):
    try:
        message = types.Content(role="user", parts=[types.Part(text=query)])
        
        with suppress_stdout_stderr():
            events = runner.run(
                user_id="web_user", 
                session_id="web_session", 
                new_message=message
            )
        
        for event in events:
            if event.is_final_response() and event.content and event.content.parts:
                return event.content.parts[0].text
        
        return "I apologize, but I couldn't process your weather request at the moment. Please try again."
    
    except Exception as e:
        return f"Sorry, there was an error processing your request: {str(e)}"

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Please enter a message'}), 400
        
        # Get response from agent
        agent_response = ask_agent(user_message)
        
        return jsonify({
            'response': agent_response,
            'timestamp': datetime.now().strftime('%H:%M')
        })
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'agent': 'weather_agent'})

# --- Main ---
if __name__ == '__main__':
    print("🌤️ Weather Agent Web Interface Starting...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🔄 The agent is ready to answer weather questions!")
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)