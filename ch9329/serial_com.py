from serial import Serial

ser = Serial("/dev/ttyUSB0", 9600, timeout=1)


def send(command: str, interval: float = 0.1):
    ser.write(command)
