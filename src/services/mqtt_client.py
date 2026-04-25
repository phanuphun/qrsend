import paho.mqtt.client as mqtt
import threading

DEFAULT_HOST  = "localhost"
DEFAULT_PORT  = 1883
DEFAULT_TOPIC = "qr/scan"

def _doPublish(message: str, topic: str, host: str, port: int):
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.connect(host, port, keepalive=60)
        result = client.publish(topic, message)
        result.wait_for_publish(timeout=5.0)
        client.disconnect()
        print(f"MQTT → [{topic}] {message}")
    except Exception as e:
        print(f"MQTT error: {e}")

def publishMessage(
    message: str,
    topic: str = DEFAULT_TOPIC,
    host: str  = DEFAULT_HOST,
    port: int  = DEFAULT_PORT,
):
    """Publish ใน background thread — ไม่ block camera loop"""
    t = threading.Thread(target=_doPublish, args=(message, topic, host, port), daemon=True)
    t.start()
