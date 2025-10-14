import RPi.GPIO as GPIO
import bluetooth
import time

# 設定GPIO模式
GPIO.setmode(GPIO.BCM)
PIR_PIN = 4     # GPIO PIN
GPIO.setup(PIR_PIN, GPIO.IN)

# 設定藍牙連接
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

print("等待藍牙接收端連接...")
client_sock, client_info = server_sock.accept()
print("接收端已連接:", client_info)

try:
    while True:
        print(GPIO.input(PIR_PIN))
        if GPIO.input(PIR_PIN):
            print("Motion Detected!")
            client_sock.send("Motion Detected!")
        else:
            print("No motion")
            client_sock.send("No motion")
        time.sleep(1)
except KeyboardInterrupt:
    print("程式已終止")
    client_sock.close()
    server_sock.close()
    GPIO.cleanup()

