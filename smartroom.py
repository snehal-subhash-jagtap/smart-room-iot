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

client.connect()
print("Connected to AWS IoT Core")

# ====== INITIAL STATES ======
temperature = 25.0
humidity = 50.0

light_state = "OFF"
fan_state = "OFF"

# ====== RECEIVE CONTROL ======
def on_control(client, userdata, message):
    global light_state, fan_state

    data = json.loads(message.payload.decode())

    if "light" in data:
        light_state = data["light"]
        print("Light changed to:", light_state)

    if "fan" in data:
        fan_state = data["fan"]
        print("Fan changed to:", fan_state)

client.subscribe("smartroom/control", 1, on_control)

# ====== LOOP ======
temperature = 25.0
humidity = 50.0

light_state = "OFF"
fan_state = "OFF"

def on_control(client, userdata, message):
    global light_state, fan_state
    data = json.loads(message.payload.decode())

    if "light" in data:
        light_state = data["light"]
        print("Light:", light_state)

    if "fan" in data:
        fan_state = data["fan"]
        print("Fan:", fan_state)

client.subscribe("smartroom/control", 1, on_control)

while True:
    # smooth temp change
    temperature += random.uniform(-0.5, 0.5)

    # 💡 light increases heat
    if light_state == "ON":
        temperature += 0.4

    # 🌀 fan cools room
    if fan_state == "ON":
        temperature -= 0.6

    temperature = max(20, min(35, temperature))
    temperature = round(temperature, 2)

    humidity += random.uniform(-1, 1)
    humidity = max(40, min(70, humidity))
    humidity = round(humidity, 2)

    payload = {
        "temperature": temperature,
        "humidity": humidity,
        "light": light_state,
        "fan": fan_state
    }

    client.publish("smartroom/data", json.dumps(payload), 1)

    shadow_payload = {"state": {"reported": payload}}
    client.publish(
        "$aws/things/SmartRoom/shadow/update",
        json.dumps(shadow_payload),
        1
    )

    print("Sent:", payload)

    time.sleep(2)