import bluetooth

bd_addr = "B8:27:EB:93:0C:5C" # Have to replace by your Raspberry Pi (Transmitter) Address
port = 1
# 搜尋附近的藍牙設備
nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("找到的藍牙設備:", nearby_devices)

# 選擇Raspberry Pi的藍牙地址
raspberry_pi_address = None
for address, name in nearby_devices:
    if address==bd_addr:
        raspberry_pi_address = address
        break

if raspberry_pi_address is None:
    print("未找到Raspberry Pi")
    exit()

# 建立藍牙連接
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((raspberry_pi_address, port))

try:
    while True:
        data = sock.recv(1024).decode('utf-8').strip()
        print("接收到的數據:", data)
except KeyboardInterrupt:
    print("程式已終止")
    sock.close()
