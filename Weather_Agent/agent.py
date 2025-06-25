import os
import sys
import json
import asyncio
import logging
import contextlib

from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from dotenv import load_dotenv
load_dotenv()



# --- Constants ---
APP_NAME = "weather_agent_app"
USER_ID = "user_001"
SESSION_ID = "session_001"
MODEL_NAME = "gemini-2.0-flash"

# --- Weather Agent ---
agent = LlmAgent(
    model=MODEL_NAME,
    name="weather_agent",
    description="Provides weather updates based on user queries.",
    instruction="""
You are a helpful assistant. When a user asks for the weather in a specific city, respond directly using your own knowledge.
""",
)

# --- Runner Setup ---
session_service = InMemorySessionService()
runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)

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

# --- Ask the Agent ---
def ask_agent(city: str):
    print(f"\n[User Input]: What is the weather in {city}?")
    message = types.Content(role="user", parts=[types.Part(text=f"What is the weather in {city}?")])

    with suppress_stdout_stderr():
        events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=message)

    for event in events:
        if event.is_final_response() and event.content and event.content.parts:
            print(f"[Agent Reply]: {event.content.parts[0].text}")
            return

    print("[Agent Reply]: No response received")

# --- Main Loop ---
def main():
    asyncio.run(session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID))
    print("Enter a city name (e.g., New York) or type 'exit' to quit.")

    while True:
        city = input("\nYour input: ").strip()
        if city.lower() == "exit":
            print("Exiting...")
            break
        if not city:
            print("Please enter a city name.")
            continue
        ask_agent(city)

if __name__ == "__main__":
    main()