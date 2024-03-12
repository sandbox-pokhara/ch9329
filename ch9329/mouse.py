from __future__ import annotations

import random
import time

from serial import Serial

from ch9329.utils import get_packet

ctrl_to_hex_mapping = {
    "null": b"\x00",
    "left": b"\x01",
    "right": b"\x02",
    "center": b"\x04",
}

HEAD = b"\x57\xab"  # Frame header
ADDR = b"\x00"  # Address
CMD = b"\x04"  # Command
LEN = b"\x07"  # Data length


def send_data_absolute(
    ser: Serial,
    x: int,
    y: int,
    ctrl: str = "null",
    x_max: int = 1920,
    y_max: int = 1080,
) -> None:
    data = b"\x02"
    data += ctrl_to_hex_mapping[ctrl]
    x_cur = (4096 * x) // x_max
    y_cur = (4096 * y) // y_max
    data += x_cur.to_bytes(2, byteorder="little")
    data += y_cur.to_bytes(2, byteorder="little")
    if len(data) < 7:
        data += b"\x00" * (7 - len(data))
    else:
        data = data[:7]
    packet = get_packet(HEAD, ADDR, CMD, LEN, data)
    ser.write(packet)


def move(
    ser: Serial,
    x: int,
    y: int,
    monitor_width: int = 1920,
    monitor_height: int = 1080,
) -> None:
    send_data_absolute(ser, x, y, "null", monitor_width, monitor_height)


def press(ser: Serial, button: str = "left") -> None:
    send_data_absolute(ser, 0, 0, button)


def release(ser: Serial) -> None:
    send_data_absolute(ser, 0, 0, "null")


def click(ser: Serial, button: str = "left") -> None:
    press(ser, button)
    # 100 to 450 milliseconds delay for simulating natural behavior
    time.sleep(random.uniform(0.1, 0.45))
    release(ser)
