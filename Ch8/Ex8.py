# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awsiot import mqtt5_client_builder
from awscrt import mqtt5
import threading, time
from serial import Serial
import json

import random, string
random_key = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))
TIMEOUT = 100
message_count = 5
message_topic = "rpi_TA/PM25"
message_string = "PM25"
endpoint = "a5g6maunbut70-ats.iot.ap-southeast-2.amazonaws.com"
clientId = "rpi_TA"
cert_path = "rpi_TA.cert.pem"
private_key_path = "rpi_TA.private.key"

# Events used within callbacks to progress sample
connection_success_event = threading.Event()
stopped_event = threading.Event()
received_all_event = threading.Event()
received_count = 0


# Callback when any publish is received
def on_publish_received(publish_packet_data):
    publish_packet = publish_packet_data.publish_packet
    print("==== Received message from topic '{}': {} ====\n".format(
        publish_packet.topic, publish_packet.payload.decode('utf-8')))

    # Track number of publishes received
    global received_count
    received_count += 1
    if received_count == message_count:
        received_all_event.set()


# Callback for the lifecycle event Stopped
def on_lifecycle_stopped(lifecycle_stopped_data: mqtt5.LifecycleStoppedData):
    print("Lifecycle Stopped\n")
    stopped_event.set()


# Callback for lifecycle event Attempting Connect
def on_lifecycle_attempting_connect(lifecycle_attempting_connect_data: mqtt5.LifecycleAttemptingConnectData):
    print("Lifecycle Connection Attempt\nConnecting to endpoint: '{}' with client ID'{}'".format(
        endpoint, clientId))


# Callback for the lifecycle event Connection Success
def on_lifecycle_connection_success(lifecycle_connect_success_data: mqtt5.LifecycleConnectSuccessData):
    connack_packet = lifecycle_connect_success_data.connack_packet
    print("Lifecycle Connection Success with reason code:{}\n".format(
        repr(connack_packet.reason_code)))
    connection_success_event.set()


# Callback for the lifecycle event Connection Failure
def on_lifecycle_connection_failure(lifecycle_connection_failure: mqtt5.LifecycleConnectFailureData):
    print("Lifecycle Connection Failure with exception:{}".format(
        lifecycle_connection_failure.exception))


# Callback for the lifecycle event Disconnection
def on_lifecycle_disconnection(lifecycle_disconnect_data: mqtt5.LifecycleDisconnectData):
    print("Lifecycle Disconnected with reason code:{}".format(
        lifecycle_disconnect_data.disconnect_packet.reason_code if lifecycle_disconnect_data.disconnect_packet else "None"))

if __name__ == '__main__':
    print("\nStarting MQTT5 X509 PubSub Sample\n")

    # Create MQTT5 client using mutual TLS via X509 Certificate and Private Key
    print("==== Creating MQTT5 Client ====\n")
    client = mqtt5_client_builder.mtls_from_path(
        endpoint=endpoint,
        cert_filepath=cert_path,
        pri_key_filepath=private_key_path,
        on_publish_received=on_publish_received,
        on_lifecycle_stopped=on_lifecycle_stopped,
        on_lifecycle_attempting_connect=on_lifecycle_attempting_connect,
        on_lifecycle_connection_success=on_lifecycle_connection_success,
        on_lifecycle_connection_failure=on_lifecycle_connection_failure,
        on_lifecycle_disconnection=on_lifecycle_disconnection,
        client_id=clientId)
    

    # Start the client, instructing the client to desire a connected state. The client will try to 
    # establish a connection with the provided settings. If the client is disconnected while in this 
    # state it will attempt to reconnect automatically.
    print("==== Starting client ====")
    client.start()

    # We await the `on_lifecycle_connection_success` callback to be invoked.
    if not connection_success_event.wait(TIMEOUT):
        raise TimeoutError("Connection timeout")

    # publish
    loopCount = 0
    ser = Serial('/dev/ttyUSB0', 9600, timeout=.5)

    try:
      while True:
        if ser.inWaiting():
          str = ser.readline().decode('utf8')[:-2]
          print(str)
          end = str.find(' :')
          if end > 0:
            PM25 = str[:end]
            message = {}
            message['key'] = random_key
            message['type'] = 'PM2.5'
            message['value'] = PM25
            message['sequence'] = loopCount
            messageJson = json.dumps(message).encode('utf-8')

            print('Published topic %s: %s\n' % (message_topic, messageJson))
            publish_future = client.publish(mqtt5.PublishPacket(
              topic=message_topic,
              payload=messageJson,
              qos=mqtt5.QoS.AT_LEAST_ONCE
            ))
            publish_completion_data = publish_future.result(TIMEOUT)
            print("PubAck received with {}\n".format(repr(publish_completion_data.puback.reason_code)))

            loopCount += 1

    except KeyboardInterrupt:

      # Stop the client. Instructs the client to disconnect and remain in a disconnected state.
      print("==== Stopping Client ====")
      client.stop()

      if not stopped_event.wait(TIMEOUT):
          raise TimeoutError("Stop timeout")

      print("==== Client Stopped! ====")
