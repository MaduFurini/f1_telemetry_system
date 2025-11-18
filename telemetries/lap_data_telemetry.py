# telemetries/lap_data.py
import struct

HEADER_SIZE = 29
CAR_COUNT = 22
LAPDATA_SIZE = 50
PACKET_ID_LAPDATA = 2


def parse_lap_data(data: bytes):
    # Confere se é mesmo Lap Data
    if data[6] != PACKET_ID_LAPDATA:
        return None

    lap_data = []
    base = HEADER_SIZE

    for i in range(CAR_COUNT):
        offset = base + i * LAPDATA_SIZE

        last_ms, current_ms = struct.unpack_from("<II", data, offset)
        sector1_ms = struct.unpack_from("<H", data, offset + 8)[0]
        sector1_min = data[offset + 10]
        sector2_ms = struct.unpack_from("<H", data, offset + 11)[0]
        sector2_min = data[offset + 13]

        delta_front_ms = struct.unpack_from("<H", data, offset + 14)[0]
        delta_leader_ms = struct.unpack_from("<H", data, offset + 16)[0]

        lap_distance = struct.unpack_from("<f", data, offset + 18)[0]
        total_distance = struct.unpack_from("<f", data, offset + 22)[0]
        safety_car_delta = struct.unpack_from("<f", data, offset + 26)[0]

        car_position = data[offset + 30]          # <- POSIÇÃO CORRETA
        current_lap_num = data[offset + 31]

        pit_status = data[offset + 32]
        num_pit_stops = data[offset + 33]
        sector = data[offset + 34]
        current_lap_invalid = data[offset + 35]
        penalties = data[offset + 36]
        total_warnings = data[offset + 37]
        corner_cut_warnings = data[offset + 38]
        num_dt = data[offset + 39]
        num_sg = data[offset + 40]
        grid_position = data[offset + 41]
        driver_status = data[offset + 42]
        result_status = data[offset + 43]
        pit_lane_timer_active = data[offset + 44]
        pit_lane_time_ms = struct.unpack_from("<H", data, offset + 45)[0]
        pit_stop_timer_ms = struct.unpack_from("<H", data, offset + 47)[0]
        pit_should_serve_pen = data[offset + 49]

        lap_data.append({
            "index": i,
            "car_position": car_position,
            "current_lap_num": current_lap_num,
            "last_lap_ms": last_ms,
            "current_lap_ms": current_ms,
            "delta_front_ms": delta_front_ms,
            "delta_leader_ms": delta_leader_ms,
            "lap_distance": lap_distance,
            "total_distance": total_distance,
            "safety_car_delta": safety_car_delta,
            "grid_position": grid_position,
            "driver_status": driver_status,
            "result_status": result_status,
            "pit_status": pit_status,
            "num_pit_stops": num_pit_stops,
            "sector": sector,
            "current_lap_invalid": current_lap_invalid,
            "penalties": penalties,
            "total_warnings": total_warnings,
            "corner_cut_warnings": corner_cut_warnings,
            "num_dt": num_dt,
            "num_sg": num_sg,
            "pit_lane_timer_active": pit_lane_timer_active,
            "pit_lane_time_ms": pit_lane_time_ms,
            "pit_stop_timer_ms": pit_stop_timer_ms,
            "pit_should_serve_pen": pit_should_serve_pen,
        })

    return lap_data
