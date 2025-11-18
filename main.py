import socket
import struct
from telemetries.drivers_telemetry import parse_participants
from telemetries.car_telemetry import parse_car_telemetry
from telemetries.lap_data_telemetry import parse_lap_data

UDP_IP = "0.0.0.0"
UDP_PORT = 20777

def format_delta(sec):
    if sec == 0 or sec is None:
        return "+0.000s"
    return f"+{sec:.3f}s"

def main():
    print(f"ESCUTANDO {UDP_IP}:{UDP_PORT}...\n")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    participants = None
    telemetry = None
    lapdata = None

    while True:
        data, addr = sock.recvfrom(2048)

        packetId = data[6]

        # PARTICIPANTS
        if packetId == 4:
            participants = parse_participants(data)
            print("[OK] Participants atualizado.")

        # TELEMETRIA
        elif packetId == 6:
            telemetry = parse_car_telemetry(data)

        # LAP DATA
        elif packetId == 2:
            lapdata = parse_lap_data(data)

        # Quando tudo estiver disponível, a gente printa
        if participants and telemetry and lapdata:
            print("\n=== GRID ATUAL ===")

            cars = []
            for i in range(22):
                name = participants[i]["name"] if i < len(participants) else f"CAR{i}"
                speed = telemetry[i]["speed"] if i < len(telemetry) else 0

                ld = lapdata[i] if i < len(lapdata) else None
                if ld:
                    pos = ld["car_position"]
                    delta_leader_s = ld["delta_leader_ms"] / 1000.0

                    last_lap = ld["last_lap_ms"] / 1000.0 if ld["last_lap_ms"] > 0 else None
                    current_lap = ld["current_lap_ms"] / 1000.0 if ld["current_lap_ms"] > 0 else None
                else:
                    pos = 99
                    delta_leader_s = 0.0

                cars.append({
                    "idx": i,
                    "name": name,
                    "pos": pos,
                    "speed": speed,
                    "delta_leader_s": delta_leader_s,
                    "last_lap": last_lap,
                    "current_lap": current_lap
                })

            # tira carros sem posição (0) e ordena por posição
            cars = [c for c in cars if c["pos"] != 0]
            cars.sort(key=lambda x: x["pos"])

            for c in cars:
                delta_str = "+0.000s" if c["delta_leader_s"] == 0 else f"+{c['delta_leader_s']:.3f}s"

                ll = f"{c['last_lap']:.3f}s" if c["last_lap"] is not None else "--.--"
                cl = f"{c['current_lap']:.3f}s" if c["current_lap"] is not None else "--.--"

                print(
                    f"{c['pos']:>2}. {c['name']:<12} "
                    f"{c['speed']:>3} km/h   {delta_str}   "
                    f"LL:{ll}   CL:{cl}"
                )

            print("=====================\n")



if __name__ == "__main__":
    main()
