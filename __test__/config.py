import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 20777

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(10):
    sock.sendto(b"teste", (UDP_IP, UDP_PORT))
    print(f"Enviado pacote {i}")
