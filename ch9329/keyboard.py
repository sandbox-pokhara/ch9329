from __future__ import annotations

import time

from serial import Serial

from ch9329.exceptions import InvalidKey
from ch9329.exceptions import InvalidModifier
from ch9329.hid import HID_KEY_SHIFT_LEFT
from ch9329.hid import HID_MAPPING
from ch9329.hid import MODIFIERS
from ch9329.utils import get_packet

# Convert character to data packet
HEAD = b"\x57\xab"  # Frame header
ADDR = b"\x00"  # Address
CMD = b"\x02"  # Command
LEN = b"\x08"  # Data length


def send(ser: Serial, key: str = "", modifier: str = "") -> None:
    data = b""

    # modifiers
    if modifier:
        if modifier not in MODIFIERS:
            raise InvalidModifier(modifier)
        hid, _ = HID_MAPPING[modifier]
        data += hid

    if key:
        if key not in HID_MAPPING:
            raise InvalidKey(key)
        hid, shift = HID_MAPPING[key]
        if shift:
            data += HID_KEY_SHIFT_LEFT
        else:
            data += b"\x00"
        data += b"\x00"
        data += hid
    else:
        data += b"\x00"

    # fill up remaining bytes
    if len(data) < 8:
        data += b"\x00" * (8 - len(data))
    else:
        data = data[:8]

    # create packet and send
    packet = get_packet(HEAD, ADDR, CMD, LEN, data)
    ser.write(packet)


def press(ser: Serial, key: str, modifier: str = "") -> None:
    send(ser, key, modifier)


def release(ser: Serial) -> None:
    send(ser, "")


def press_and_release(ser: Serial, key: str, modifier: str = "") -> None:
    press(ser, key, modifier)
    release(ser)


def write(ser: Serial, text: str, interval: float = 0.1) -> None:
    for char in text:
        press_and_release(ser, char)
        time.sleep(interval)
