import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 20777
BUFFER_SIZE = 2048

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    try:
        data, addr = sock.recvfrom(BUFFER_SIZE)
    except socket.timeout:
        continue
    print(f"Recebi {len(data)} bytes de {addr}")