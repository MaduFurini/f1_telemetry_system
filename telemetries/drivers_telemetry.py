import struct

HEADER_SIZE = 29
CAR_COUNT = 22
PARTICIPANT_SIZE = 58     # confirmado pelo dump real

PACKET_ID_PARTICIPANTS = 4

def parse_participants(data):
    if data[6] != PACKET_ID_PARTICIPANTS:
        return None

    participants = []
    base = HEADER_SIZE

    for i in range(CAR_COUNT):
        offset = base + i * PARTICIPANT_SIZE

        ai_controlled = data[offset + 0]
        driver_id      = data[offset + 1]
        team_id        = data[offset + 2]
        race_number    = data[offset + 3]
        nationality    = struct.unpack_from("<H", data, offset + 4)[0]

        name_bytes = data[offset + 8 : offset + 8 + 48]
        name = bytes(name_bytes).decode("utf-8", errors="ignore").rstrip("\x00")

        participants.append({
            "index": i,
            "name": name,
            "race_number": race_number,
            "team_id": team_id,
            "driver_id": driver_id,
            "nationality": nationality,
            "is_ai": ai_controlled,
        })

    return participants
