from enum import Enum

from serial import Serial
from utils import get_packet

HEAD = b"\x57\xab"  # Frame header
ADDR = b"\x00"  # Address

CMD_GET_PARA_CFG = b"\x08"
LEN_GET_PARA_CFG = b"\x00"
DATA_GET_PARA_CFG = b""

CMD_SET_PARA_CFG = b"\x09"
LEN_SET_PARA_CFG = b"\x32"

USB_STRING_ENABLE_FLAG = b"\x87"

CMD_GET_USB_STRING = b"\x0a"
LEN_GET_USB_STRING = b"\x01"


class USBStringDescriptor(Enum):
    MANUFACTURER = b"\x00"
    PRODUCT = b"\x01"
    SERIAL_NUMBER = b"\x02"


CMD_SET_USB_STRING = b"\x0b"


def set_device_descriptors(
    ser: Serial, descriptor_type: USBStringDescriptor, description: str
):
    if (
        len(description) > 23
    ):  # length of description should not be more than 23
        return False

    description_bytes = description.encode("utf-8")
    packet = get_packet(
        HEAD,
        ADDR,
        CMD_GET_USB_STRING,
        LEN_GET_USB_STRING,
        descriptor_type.value,
    )
    ser.write(packet)
    ser.readline()  # Read the response packet

    # Construct the packet for CMD_SET_USB_STRING
    descriptor_length = len(description_bytes)
    if descriptor_length == 0:
        descriptor_length = (
            1  # Ensure there's at least one byte for an empty string
        )

    modified_data = (
        bytes([descriptor_type.value[0]])
        + bytes([descriptor_length])
        + description_bytes
    )

    modified_packet = get_packet(
        HEAD,
        ADDR,
        CMD_SET_USB_STRING,
        bytes([len(modified_data)]),
        modified_data,
    )
    ser.write(modified_packet)
    return_packet = ser.readline()
    # this packet is expected in response when the VID and PID are
    # successfully set
    expected_packet = b"W\xab\x00\x8b\x01\x00\x8e"
    return return_packet == expected_packet  # Compare and return result


def set_device_ids(
    ser: Serial, vid: int, pid: int, custom_descriptor: bool = False
) -> bool:
    # this packet is sent to ch9329 in response to which it sends the
    # current configuration
    packet = get_packet(
        HEAD, ADDR, CMD_GET_PARA_CFG, LEN_GET_PARA_CFG, DATA_GET_PARA_CFG
    )
    ser.write(packet)
    received_packet = ser.readline()  # read the current configuration
    vid_bytes = vid.to_bytes(
        2, "little"
    )  # Convert VID to little-endian 2-byte format
    pid_bytes = pid.to_bytes(
        2, "little"
    )  # Convert PID to little-endian 2-byte format
    modified_data = (
        received_packet[5:16] + vid_bytes + pid_bytes + received_packet[20:55]
    )  # Replace VID and PID bytes
    if custom_descriptor:
        modified_data = (
            modified_data[:35] + USB_STRING_ENABLE_FLAG + modified_data[36:]
        )
    modified_packet = get_packet(
        HEAD, ADDR, CMD_SET_PARA_CFG, LEN_SET_PARA_CFG, modified_data
    )
    # Send modified packet with the new VID and PID
    ser.write(modified_packet)
    return_packet = ser.readline()  # Read the response packet
    # this packet is expected in response when the VID and PID are
    # successfully set
    expected_packet = b"W\xab\x00\x89\x01\x00\x8c"
    return return_packet == expected_packet  # Compare and return result
