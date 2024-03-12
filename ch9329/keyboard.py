import time

from serial import Serial

from ch9329.ascii_to_ch9329 import HID_KEY_ALT_LEFT
from ch9329.ascii_to_ch9329 import HID_KEY_ALT_RIGHT
from ch9329.ascii_to_ch9329 import HID_KEY_CONTROL_LEFT
from ch9329.ascii_to_ch9329 import HID_KEY_CONTROL_RIGHT
from ch9329.ascii_to_ch9329 import HID_KEY_GUI_LEFT
from ch9329.ascii_to_ch9329 import HID_KEY_GUI_RIGHT
from ch9329.ascii_to_ch9329 import HID_KEY_SHIFT_LEFT
from ch9329.ascii_to_ch9329 import HID_KEY_SHIFT_RIGHT
from ch9329.ascii_to_ch9329 import conv_table
from ch9329.exceptions import InvalidModifier
from ch9329.utils import get_packet

# Convert character to data packet
HEAD = b"\x57\xab"  # Frame header
ADDR = b"\x00"  # Address
CMD = b"\x02"  # Command
LEN = b"\x08"  # Data length


def get_modifier_keycode(key: str):
    if key == "ctrl":
        return HID_KEY_CONTROL_LEFT
    if key == "control_left":
        return HID_KEY_CONTROL_LEFT
    if key == "shift":
        return HID_KEY_SHIFT_LEFT
    if key == "shift_left":
        return HID_KEY_SHIFT_LEFT
    if key == "alt_left":
        return HID_KEY_ALT_LEFT
    if key == "gui_left":
        return HID_KEY_GUI_LEFT
    if key == "control_right":
        return HID_KEY_CONTROL_RIGHT
    if key == "shift_right":
        return HID_KEY_SHIFT_RIGHT
    if key == "alt_right":
        return HID_KEY_ALT_RIGHT
    if key == "gui_right":
        return HID_KEY_GUI_RIGHT
    raise InvalidModifier


# Function to convert ASCII characters to HID keycodes
def get_ascii_keycode(key: str) -> tuple[int, bytes]:
    ascii_val = ord(key)  # Get ASCII value of character
    shift, keycode = conv_table[ascii_val]
    return shift, keycode


def send(ser: Serial, key: str = "", modifier: str = "") -> None:
    data = b""

    # modifiers
    if modifier == "":
        pass
    else:
        hid = get_modifier_keycode(modifier)
        data += hid

    # ascii keys
    if key:
        shift, keycode = get_ascii_keycode(key)
        if shift:
            data += HID_KEY_SHIFT_LEFT
        else:
            data += b"\x00"
        data += b"\x00"
        data += keycode
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
