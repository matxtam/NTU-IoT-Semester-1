import bluetooth
import socket

# 藍牙設定
bt_addr = "B8:27:EB:93:0C:5C"  # TODO Change to your Tx raspberry pi address
port_bt = 1

# TCP設定
TCP_IP = '127.0.0.1'
TCP_PORT = 1337
BUFFER_SIZE = 1024

# 建立TCP連接
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.connect((TCP_IP, TCP_PORT))

# 搜尋附近的藍牙設備
nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("找到的藍牙設備:", nearby_devices)

# 選擇Raspberry Pi的藍牙地址
raspberry_pi_address = None
for address, name in nearby_devices:
    if address == bt_addr:
        raspberry_pi_address = address
        break

if raspberry_pi_address is None:
    print("未找到Raspberry Pi")
    exit()

# 建立藍牙連接
bt_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
bt_sock.connect((raspberry_pi_address, port_bt))

try:
    while True:
        data = bt_sock.recv(1024).decode('utf-8').strip()
        print("接收到的數據:", data)
        
        # 將接收到的藍牙數據透過TCP發送
        tcp_sock.send(data.encode('utf-8'))
except KeyboardInterrupt:
    print("程式已終止")
    bt_sock.close()
    tcp_sock.close()