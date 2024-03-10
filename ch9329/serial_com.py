from serial import Serial


def send(command: str, interval: float = 0.1):
    with Serial("/dev/ttyUSB0", 9600, timeout=1) as ser:
        ser.write(command)
