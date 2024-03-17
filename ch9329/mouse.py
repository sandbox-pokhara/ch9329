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
CMD_ABS = b"\x04"  # Command for absolute
CMD_REL = b"\x05"  # Command for relative
LEN_ABS = b"\x07"  # Data length for absolute
LEN_REL = b"\x05"  # Data length for relative


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
    packet = get_packet(HEAD, ADDR, CMD_ABS, LEN_ABS, data)
    ser.write(packet)


def send_data_relative(
    ser: Serial, x: int, y: int, ctrl: str = "null"
) -> None:
    data = b"\x01"
    data += ctrl_to_hex_mapping[ctrl]
    if x < 0:
        data += (0 - abs(x)).to_bytes(1, byteorder="big", signed=True)
    else:
        data += x.to_bytes(1, byteorder="big", signed=True)

    if y < 0:
        data += (0 - abs(y)).to_bytes(1, byteorder="big", signed=True)
    else:
        data += y.to_bytes(1, byteorder="big", signed=True)

    data += b"\x00" * (5 - len(data)) if len(data) < 5 else data[:5]

    packet = get_packet(HEAD, ADDR, CMD_REL, LEN_REL, data)
    ser.write(packet)


def move(
    ser: Serial,
    x: int,
    y: int,
    relative: bool = False,
    monitor_width: int = 1920,
    monitor_height: int = 1080,
) -> None:
    if relative:
        send_data_relative(ser, x, y, "null")
    else:
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
