# Weather-Agent-App

🌤️ Weather Agent Chatbot 🌐
A smart weather-aware chatbot built using Flask and HTML/CSS/JavaScript that provides real-time weather updates and conversational interactions with users. Designed with a dynamic weather-themed interface, this chatbot makes accessing weather data both intuitive and visually engaging.

🚀 Features
💬 Interactive Chat Interface: Ask about today’s weather, tomorrow’s forecast, or general weather conditions.

🌦️ Real-Time Weather Data: Fetches live weather information using external APIs (e.g., Gemini API).

🎨 Weather-Based UI: Background and styling change based on the current climate (sunny, rainy, cloudy, etc.).

⚙️ Flask-Powered Backend: Handles chatbot logic and weather data processing.

🌐 Responsive Web Interface: Works across devices—desktops, tablets, and smartphones.

🛠️ Tech Stack
Frontend: HTML, CSS, JavaScript

Backend: Python (Flask)

Hosting: Flask local server / Deployable to Render, Replit, or Heroku

📷 Screenshots

![Screenshot 2025-06-25 092917](https://github.com/user-attachments/assets/c4efe581-07ab-41d3-a6cf-b228682d8488)


📁 Folder Structure
bash
Copy code
Weather_Agent/
├── templates/
│   └── index.html
├── app.py
|-- agent.py
├── requirements.txt
└── README.md
🧠 How It Works
User sends a message through the chatbot UI.

The message is sent to the Flask backend.

Flask interprets the request, fetches weather data, and formulates a reply.

The chatbot displays the response and updates the background accordingly.

🧪 Try It Out
bash
Copy code
git clone https://github.com/your-username/weather-agent-chatbot.git
cd Weather_Agent
pip install -r requirements.txt
python app.py
Open http://127.0.0.1:5000 in your browser to chat with the Weather Agent! 🌍

🤝 Contributions
Feel free to fork this repository and contribute to future features like:

This Agent is response only weather report of specific City.(e.g., Trichy, Chennai, karur etc..)

📜 License
This project is licensed under the MIT License.
