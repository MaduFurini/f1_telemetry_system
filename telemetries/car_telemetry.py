# telemetries/car_telemetry.py
import struct

HEADER_SIZE = 29          # tamanho exato do PacketHeader
CAR_SIZE = 60             # tamanho de cada CarTelemetryData
PACKET_ID_CAR_TELEMETRY = 6

def parse_car_telemetry(data: bytes):
    # Garante que é grande o suficiente
    if len(data) < HEADER_SIZE + CAR_SIZE:
        return None

    # packet_id fica no byte 6 (0-based)
    packet_id = data[6]
    if packet_id != PACKET_ID_CAR_TELEMETRY:
        return None

    # índice do carro do jogador: byte 27
    player_car_index = data[27]

    # início do bloco do carro do jogador
    base = HEADER_SIZE + CAR_SIZE * player_car_index

    # também garante que não vamos estourar o buffer
    if base + CAR_SIZE > len(data):
        return None

    # Campos principais
    speed = struct.unpack_from("<H", data, base + 0)[0]   
    throttle = struct.unpack_from("<f", data, base + 2)[0]
    steer = struct.unpack_from("<f", data, base + 6)[0]
    brake = struct.unpack_from("<f", data, base + 10)[0]
    clutch = struct.unpack_from("<B", data, base + 14)[0]
    gear = struct.unpack_from("<b", data, base + 15)[0]
    rpm = struct.unpack_from("<H", data, base + 16)[0]
    drs = struct.unpack_from("<B", data, base + 18)[0]

    return {
        "player_car_index": player_car_index,
        "speed": speed,
        "throttle": throttle,
        "steer": steer,
        "brake": brake,
        "clutch": clutch,
        "gear": gear,
        "rpm": rpm,
        "drs": drs,
    }
