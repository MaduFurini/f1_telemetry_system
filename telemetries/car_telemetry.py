import struct

def parse_car_telemetry(data):
    print("CHEGO")
    # Ignorando o cabeçalho (24 bytes)
    offset = 24
    
    # Car 0: velocidade (unsigned short = 2 bytes)
    speed = struct.unpack_from('<H', data, offset)[0]
    offset += 2
    
    # RPM (unsigned short = 2 bytes)
    rpm = struct.unpack_from('<H', data, offset)[0]
    offset += 2
    
    return speed, rpm