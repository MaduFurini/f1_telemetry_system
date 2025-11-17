import socket
from configs.config import UDP_IP, UDP_PORT, BUFFER_SIZE
from telemetries.car_telemetry import parse_car_telemetry

def run():
    print("Iniciando...")

    # Cria socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
    sock.bind((UDP_IP, UDP_PORT))
    sock.settimeout(1.0) 

    print("Aguardando pacotes UDP do F1 23...")

    try:
        while True:
            try:
                data, addr = sock.recvfrom(BUFFER_SIZE)
                speed, rpm = parse_car_telemetry(data)
                print(f"Velocidade do carro 0: {speed} km/h, RPM: {rpm}")
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")
    finally:
        sock.close()

if __name__ == "__main__":
    run()
