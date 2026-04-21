🧠 Smart Room IoT System (AWS + Python + Flask)
📌 Overview

This project is a real-time Smart Room monitoring and control system built using AWS IoT Core, Python, and Flask.

It collects environmental sensor data (temperature, humidity, light status), sends it to AWS IoT Core using MQTT protocol, and visualizes it on a live web dashboard with control capabilities.

🚀 Features

📡 Real-time data publishing using AWS IoT Core
📊 Live dashboard with temperature & humidity graph
🚨 Smart alert system (threshold-based warnings)
🎛️ Remote control of light (ON/OFF)
🔄 Bidirectional IoT communication
🌐 Professional web UI (Flask + Chart.js)
🏗️ Architecture
Python Sensor → AWS IoT Core → Flask Dashboard → Browser UI
                        ↑
                Control Commands
🛠️ Technologies Used
Python
AWS IoT Core (MQTT)
Flask
Chart.js
HTML/CSS/JavaScript

📂 Project Structure
SmartRoom/
│── smartroom.py        # IoT device simulator (publisher + subscriber)
│── dashboard.py        # Flask web dashboard
│── certs/              # AWS IoT certificates (NOT uploaded to GitHub)

⚙️ How to Run
1. Install dependencies
pip install flask AWSIoTPythonSDK
2. Run IoT device
python smartroom.py
3. Run dashboard
python dashboard.py
4. Open browser
http://127.0.0.1:5000

🔐 Security Note
AWS IoT certificates are not included in this repository for security reasons.

🎯 Future Improvements
Mobile app integration
Cloud database storage (DynamoDB)
AI-based anomaly detection
Multi-room IoT system

👨‍💻 Author
Snehal Jagtap
