from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time
import random

# ====== CONFIG ======
client = AWSIoTMQTTClient("SmartRoomDevice")

client.configureEndpoint(
    "a3q2r3lwwu9ova-ats.iot.eu-north-1.amazonaws.com", 8883
)

client.configureCredentials(
    "certs/AmazonRootCA1.pem",
    "certs/private.pem.key",
    "certs/certificate.pem.crt"
)

# ====== CONNECT ======
client.connect()
print("Connected to AWS IoT Core")

# ====== SEND DATA LOOP ======
while True:
    payload = {
        "temperature": round(random.uniform(20, 35), 2),
        "humidity": round(random.uniform(40, 70), 2),
        "light": "ON"
    }

    client.publish("smartroom/data", json.dumps(payload), 1)

    print("Sent:", payload)

    time.sleep(5)