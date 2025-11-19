''' This is for the RPi Publisher'''
from serial import Serial
import paho.mqtt.client as paho
from time import sleep
import json

AllowedActions = ['both', 'publish', 'subscribe']
broker = "your broker ip" # [To Do]
port = # your broker port # [To Do]
clientId = "myRPi"
topic = "RPi/PM25"
mode = "publish"
client = paho.Client(client_id = clientId, callback_api_version=paho.CallbackAPIVersion.VERSION1)

# Custom MQTT message callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Connection failed")


def on_publish(client, messageJson, mid):
    if mode == 'publish':
        print('Published topic %s: %s\n' % (topic, mid))


client.on_connect = on_connect
client.on_publish = on_publish
print("try connect")
client.connect(broker,port)
sleep(2)

loopCount = 0
ser = Serial('/dev/ttyUSB0', 9600, timeout=.5)

while True:
    if ser.inWaiting():
        str = ser.readline().decode('utf8')[:-2]
        end = str.find(':')
        if end > 0:
            PM25 = str[:end]
            message = {}
            message['type'] = 'PM2.5'
            message['value'] = PM25
            message['device'] = 'RPi'
            message['sequence'] = loopCount
            messageJson = json.dumps(message)
            client.publish(topic, messageJson, 0)
            sleep(1)
            loopCount += 1

