from flask import Flask, jsonify, render_template_string
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from flask import request
import json

app = Flask(__name__)

# 🔥 added fan
latest_data = {
    "temperature": 0,
    "humidity": 0,
    "light": "OFF",
    "fan": "OFF"
}

# ---------------- AWS IoT CONFIG ----------------
client = AWSIoTMQTTClient("SmartRoomDashboard")

client.configureEndpoint("a3q2r3lwwu9ova-ats.iot.eu-north-1.amazonaws.com", 8883)

client.configureCredentials(
    "certs/AmazonRootCA1.pem",
    "certs/private.pem.key",
    "certs/certificate.pem.crt"
)

client.connect()

# ---------------- CALLBACK ----------------
def on_message(client, userdata, message):
    global latest_data

    payload = json.loads(message.payload.decode("utf-8"))
    latest_data = payload
    print("Received:", latest_data)

client.subscribe("smartroom/data", 1, on_message)

# ---------------- FLASK UI ----------------
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Room Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        body {
            font-family: Arial;
            background: #f4f6f9;
            text-align: center;
            margin: 0;
            padding: 0;
        }

        .container {
            padding: 20px;
        }

        .card {
            background: white;
            display: inline-block;
            padding: 20px;
            margin: 10px;
            border-radius: 10px;
            width: 200px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        }

        h1 {
            background: #2c3e50;
            color: white;
            padding: 15px;
            margin: 0;
        }

        .alert {
            font-weight: bold;
            margin-top: 10px;
        }

        button {
            padding: 10px 15px;
            margin: 5px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        .on {
            background: #27ae60;
            color: white;
        }

        .off {
            background: #e74c3c;
            color: white;
        }

        canvas {
            margin-top: 20px;
            background: white;
            border-radius: 10px;
            padding: 10px;
        }
    </style>
</head>

<body onload="init()">

<h1>Smart Room Control Dashboard</h1>

<div class="container">

    <div class="card">
        <h3>Temperature</h3>
        <h2 id="temp">0</h2>
    </div>

    <div class="card">
        <h3>Humidity</h3>
        <h2 id="hum">0</h2>
    </div>

    <div class="card">
        <h3>Light</h3>
        <h2 id="light">OFF</h2>
    </div>

    <!-- 🔥 NEW FAN CARD -->
    <div class="card">
        <h3>Fan</h3>
        <h2 id="fan">OFF</h2>
    </div>

    <div class="alert" id="alert"></div>

    <h3>Control Panel</h3>

    <button class="on" onclick="sendCommand('ON')">Light ON</button>
    <button class="off" onclick="sendCommand('OFF')">Light OFF</button>

    <!-- 🔥 NEW FAN BUTTONS -->
    <button class="on" onclick="sendFan('ON')">Fan ON</button>
    <button class="off" onclick="sendFan('OFF')">Fan OFF</button>

    <canvas id="tempChart" width="500" height="200"></canvas>

</div>

<script>
    let tempChart;
    let labels = [];
    let tempData = [];

    function init() {
        const ctx = document.getElementById('tempChart').getContext('2d');

        tempChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Temperature (°C)',
                    data: tempData,
                    borderWidth: 2,
                    fill: false
                }]
            },
            options: {
                scales: {
                    y: {
                        min: 20,
                        max: 40
                    }
                }
            }
        });

        setInterval(fetchData, 2000);
    }

    async function fetchData() {
        const res = await fetch('/data');
        const data = await res.json();

        document.getElementById("temp").innerText = data.temperature;
        document.getElementById("hum").innerText = data.humidity;
        document.getElementById("light").innerText = data.light;

        // 🔥 show fan
        document.getElementById("fan").innerText = data.fan;

        let alertBox = document.getElementById("alert");

        if (data.temperature > 30) {
            alertBox.innerText = "🔴 High Temperature Alert!";
            alertBox.style.color = "red";
        }
        else if (data.humidity > 70) {
            alertBox.innerText = "⚠ High Humidity Alert!";
            alertBox.style.color = "orange";
        }
        else {
            alertBox.innerText = "🟢 All Conditions Normal";
            alertBox.style.color = "green";
        }

        let time = new Date().toLocaleTimeString();

        labels.push(time);
        tempData.push(data.temperature);

        if (labels.length > 10) {
            labels.shift();
            tempData.shift();
        }

        tempChart.update();
    }

    async function sendCommand(state) {
        await fetch('/control', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ light: state })
        });

        alert("Light command sent: " + state);
    }

    // 🔥 NEW FAN FUNCTION
    async function sendFan(state) {
        await fetch('/control', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ fan: state })
        });

        alert("Fan command sent: " + state);
    }
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/data")
def data():
    return jsonify(latest_data)

@app.route("/control", methods=["POST"])
def control():
    data = request.json
    command = json.dumps(data)

    client.publish("smartroom/control", command, 1)
    print("Sent command:", command)

    return "OK"

if __name__ == "__main__":
    app.run(debug=True)