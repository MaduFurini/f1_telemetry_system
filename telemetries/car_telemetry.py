# telemetries/car_telemetry.py
import struct

HEADER_SIZE = 29
CAR_SIZE = 60
PACKET_ID_TELEMETRY = 6

def parse_car_telemetry(data):
    if data[6] != PACKET_ID_TELEMETRY:
        return None

    player_car_index = data[27]  # confirmamos!

    telemetry = []

    for i in range(22):
        base = HEADER_SIZE + CAR_SIZE * i

        speed = struct.unpack_from("<H", data, base)[0]

        telemetry.append({
            "index": i,
            "speed": speed,
        })

    return telemetry
