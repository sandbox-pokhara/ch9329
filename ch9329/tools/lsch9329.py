import serial.serialutil
import serial.tools.list_ports
from serial import Serial

from ch9329.config import get_serial_number


def main():
    comports = serial.tools.list_ports.comports()
    comports = [i for i in comports if i.vid == 6790 and i.pid == 29987]
    print(f"{len(comports)} ch9329 found.")
    for i in serial.tools.list_ports.comports():
        if i.vid == 6790 and i.pid == 29987:
            try:
                ser = Serial(i.device, 9600, timeout=0.05)
                serial_number = get_serial_number(ser)
                print(
                    f"serial_number={serial_number}, "
                    f"device={i.device}, "
                    f"location={i.location}"
                )
                ser.close()
            except serial.serialutil.SerialException:
                print(
                    f"serial_number=error, "
                    f"device={i.device}, "
                    f"location={i.location}"
                )


if __name__ == "__main__":
    main()
