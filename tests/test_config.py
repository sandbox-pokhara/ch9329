import pytest
from unittest.mock import Mock
from ch9329.config import *


def test_set_device_descriptors_raises_for_too_long_descriptor():
    with pytest.raises(ValueError):
        ser = Mock()
        set_device_descriptors(
            ser, USBStringDescriptor.MANUFACTURER, "long" * 50
        )


def test_get_parameters_returns_bytes_like_object():
    serial_response = bytes.fromhex("57ab0088328080000000258008000003861a29e100000001000d000000000000000000000000000000000000000000000000000000000024")
    ser = Mock()
    ser.readall.return_value = serial_response
    response = get_parameters(ser)
    assert response[0] == 0x57
    assert response.hex() == serial_response.hex()


def test_get_set_field_on_configuration():
    serial_response = bytes.fromhex("57ab0088328080000000258008000003861a29e100000001000d000000000000000000000000000000000000000000000000000000000024")
    #                                HEAD  CMD WM  CA        RSVD    VID     UTI     AE                                SE  RESERVED5566778899101112
    #                                    ADR LEN CM  BAUD        PINT    PID     RDT   CR CH1  CR CH2  FLT ST  FLT END   FU                        CS

    config = Configuration(serial_response)
    assert config.chip_working_mode == 0x80
    assert config.serial_comm_mode == 0x80
    assert config.serial_comm_address == 0x00
    assert config.serial_comm_baud_rate == 9600
    assert config.serial_comm_packet_interval == 3
    assert config.usb_vid == 0x1a86
    assert config.usb_pid == 0xe129
    assert config.usb_keyboard_upload_interval == 0
    assert config.usb_keyboard_release_delay == 1

    config.chip_working_mode = 1
    config.serial_comm_mode = 2
    config.serial_comm_address = 3
    config.serial_comm_baud_rate = 0x4455
    config.serial_comm_packet_interval = 0x6677
    config.usb_vid = 0x8899
    config.usb_pid = 0xaabb
    config.usb_keyboard_upload_interval = 0xccdd
    config.usb_keyboard_release_delay = 0xeeff
    config.usb_keyboard_automatic_return = 1
    config.usb_string_enable = 2
    config.usb_fast_upload = 3

    assert config.hex() == "57ab00883201020300004455080066779988bbaaccddeeff010d000000000000000000000000000000020300000000000000000000000024"
    #                        0 1 2 3 4 5 6 7 8 910111213141516171819202122232425262728293031323334353637383940414243444546474849505152535455
    #                       HEAD  CMD WM  CA        RSVD    VID     UTI     AE                                SE  RESERVED5566778899101112
    #                           ADR LEN CM  BAUD        PINT    PID     RDT   CR CH1  CR CH2  FLT ST  FLT END   FU                        CS
