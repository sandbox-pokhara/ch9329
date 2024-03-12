from ascii_to_ch9329 import HID_KEY_ALT_LEFT
from ascii_to_ch9329 import HID_KEY_ALT_RIGHT
from ascii_to_ch9329 import HID_KEY_CONTROL_LEFT
from ascii_to_ch9329 import HID_KEY_CONTROL_RIGHT
from ascii_to_ch9329 import HID_KEY_GUI_LEFT
from ascii_to_ch9329 import HID_KEY_GUI_RIGHT
from ascii_to_ch9329 import HID_KEY_SHIFT_LEFT
from ascii_to_ch9329 import HID_KEY_SHIFT_RIGHT
from ascii_to_ch9329 import conv_table
from serial import Serial


# Function to convert ASCII characters to HID keycodes
def ascii_to_ch9329(key: str):
    if key == "control_left":
        return 0, HID_KEY_CONTROL_LEFT
    elif key == "shift_left":
        return 0, HID_KEY_SHIFT_LEFT
    elif key == "alt_left":
        return 0, HID_KEY_ALT_LEFT
    elif key == "gui_left":
        return 0, HID_KEY_GUI_LEFT
    elif key == "control_right":
        return 0, HID_KEY_CONTROL_RIGHT
    elif key == "shift_right":
        return 0, HID_KEY_SHIFT_RIGHT
    elif key == "alt_right":
        return 0, HID_KEY_ALT_RIGHT
    elif key == "gui_right":
        return 0, HID_KEY_GUI_RIGHT

    ascii_val = ord(key)  # Get ASCII value of character
    if ascii_val < len(
        conv_table
    ):  # Check if the ASCII value is within the range of the conversion table
        shift, keycode = conv_table[ascii_val]
        return keycode, shift
    else:
        return None


def press(ser: Serial, key: str, ctrl: str = "") -> None:
    # Convert character to data packet
    HEAD = b"\x57\xab"  # Frame header
    ADDR = b"\x00"  # Address
    CMD = b"\x02"  # Command
    LEN = b"\x08"  # Data length
    DATA = b""  # Data

    # Control key
    if ctrl == "":
        pass
    elif isinstance(ctrl, int):
        DATA += bytes([ctrl])
    else:
        result = ascii_to_ch9329(ctrl)
        if result is not None:
            _, ctrl = result
            if ctrl:
                DATA += ctrl

    # Read data
    if len(key) >= 1:
        result = ascii_to_ch9329(key)
        if result is not None:
            keycode, shift = result
            if shift:
                DATA += HID_KEY_SHIFT_LEFT
            else:
                DATA += b"\x00"
            DATA += b"\x00"
            DATA += keycode
        else:
            DATA += b"\x00"
    else:
        DATA += b"\x00"

    if len(DATA) < 8:
        DATA += b"\x00" * (8 - len(DATA))
    else:
        DATA = DATA[:8]

    # Split the values in HEAD and calculate their sum
    HEAD_hex_list = []
    for byte in HEAD:
        HEAD_hex_list.append(byte)
    HEAD_add_hex_list = sum(HEAD_hex_list)

    # Split the values in DATA and calculate their sum
    DATA_hex_list = []
    for byte in DATA:
        DATA_hex_list.append(byte)
    DATA_add_hex_list = sum(DATA_hex_list)

    #
    try:
        SUM = (
            sum(
                [
                    HEAD_add_hex_list,
                    int.from_bytes(ADDR, byteorder="big"),
                    int.from_bytes(CMD, byteorder="big"),
                    int.from_bytes(LEN, byteorder="big"),
                    DATA_add_hex_list,
                ]
            )
            % 256
        )  # Checksum
    except OverflowError:
        print("int too big to convert")
        return False
    packet = HEAD + ADDR + CMD + LEN + DATA + bytes([SUM])  # Data packet
    ser.write(packet)


def release(ser: Serial) -> None:
    press(ser=ser, key="")


def press_and_release(ser: Serial, key: str, ctrl: str = "") -> None:
    press(ser=ser, key=key, ctrl=ctrl)
    release(ser=ser)


def write(ser: Serial, text: str) -> None:
    for char in text:
        press_and_release(ser=ser, key=char)
