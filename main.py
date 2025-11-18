# main.py
import socket
from telemetries.car_telemetry import parse_car_telemetry

UDP_IP = "127.0.0.1"
UDP_PORT = 20777
BUFFER_SIZE = 2048

def run():
    print("Aguardando telemetria do F1 23...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((UDP_IP, UDP_PORT))

    try:
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)

            tele = parse_car_telemetry(data)
            if not tele:
                continue 

            print(
                f"Carro {tele['player_car_index']} | "
                f"Vel: {tele['speed']} km/h | "
                f"RPM: {tele['rpm']} | "
                f"Marcha: {tele['gear']} | "
                f"Throttle: {tele['throttle']:.2f} | "
                f"Brake: {tele['brake']:.2f} | "
                f"DRS: {'ON' if tele['drs'] else 'OFF'}"
            )
    finally:
        sock.close()

if __name__ == "__main__":
    run()
