import random
import time

from serial import Serial
from serial_com import send

hex_dict = {"ST": b"\x02", "NU": b"\x00", "LE": b"\x01", "RI": b"\x02", "CE": b"\x04"}


def send_data_absolute(x: int, y: int, ctrl: str = "", X_MAX=1920, Y_MAX=1080) -> None:
    HEAD = b"\x57\xAB"  # Frame header
    ADDR = b"\x00"  # Address
    CMD = b"\x04"  # Command
    LEN = b"\x07"  # Data length
    DATA = bytearray(b"\x02")  # Data

    if ctrl == "":
        DATA.append(0)
    elif isinstance(ctrl, int):
        DATA.append(ctrl)
    else:
        DATA += hex_dict[ctrl]

    X_Cur = (4096 * x) // X_MAX
    Y_Cur = (4096 * y) // Y_MAX
    DATA += X_Cur.to_bytes(2, byteorder="little")
    DATA += Y_Cur.to_bytes(2, byteorder="little")

    if len(DATA) < 7:
        DATA += b"\x00" * (7 - len(DATA))
    else:
        DATA = DATA[:7]

    HEAD_hex_list = list(HEAD)
    HEAD_add_hex_list = sum(HEAD_hex_list)

    DATA_hex_list = list(DATA)
    DATA_add_hex_list = sum(DATA_hex_list)

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
        )
    except OverflowError:
        print("int too big to convert")
    packet = HEAD + ADDR + CMD + LEN + DATA + bytes([SUM])
    send(packet)


def move(x: int, y: int, monitor_width=1920, monitor_height=1080) -> None:
    send_data_absolute(x=x, y=y, X_MAX=monitor_width, Y_MAX=monitor_height)


def press(button: str) -> None:
    send_data_absolute(x=0, y=0, ctrl=button)


def release() -> None:
    send_data_absolute(x=0, y=0, ctrl="NU")


def click(button: str) -> None:
    send_data_absolute(x=0, y=0, ctrl=button)
    time.sleep(
        random.uniform(0.1, 0.45)
    )  # 100 to 450 milliseconds delay for simulating natural behavior
    send_data_absolute(x=0, y=0, ctrl="NU")
