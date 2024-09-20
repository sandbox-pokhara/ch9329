# ch9329

Python module to control ch9329

## Installation

You can install the package via pip:

```bash
pip install ch9329
```

## Usage

```py
from serial import Serial

from ch9329 import keyboard
from ch9329 import mouse
from ch9329.config import get_manufacturer
from ch9329.config import get_parameters
from ch9329.config import get_product
from ch9329.config import get_serial_number

ser = Serial("COM3", 9600, timeout=0.05)

keyboard.press_and_release(ser, "a", modifiers=["ctrl"])
keyboard.write(ser, "Hello World\n")
keyboard.write(ser, "abcdefghijklmnopqrstuvwxyz\n")
keyboard.write(ser, "ABCDEFGHIJKLMNOPQRSTUVWXYZ\n")
keyboard.write(ser, "0123456789\n")
keyboard.write(ser, "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~\n")

mouse.move(ser, x=500, y=500)
mouse.move(ser, x=50, y=50, relative=True)
mouse.click(ser, button="left")

print(get_serial_number(ser))
# 20193152CFBF
print(get_product(ser))
# WCH UART TO KB-MS_V1.7
print(get_manufacturer(ser))
# WWW.WCH.CN

params = get_parameters(ser)
print(f"cmd: {params.cmd}")
print(f"chip_working_mode: {params.chip_working_mode}")
print(f"serial_comm_mode: {params.serial_comm_mode}")
print(f"serial_comm_address: {params.serial_comm_address}")
print(f"serial_comm_baud_rate: {params.serial_comm_baud_rate}")
print(f"serial_comm_packet_interval: {params.serial_comm_packet_interval}")
print(f"usb_vid: {params.usb_vid}")
print(f"usb_pid: {params.usb_pid}")
print(f"usb_keyboard_upload_interval: {params.usb_keyboard_upload_interval}")
print(f"usb_keyboard_release_delay: {params.usb_keyboard_release_delay}")
print(f"usb_keyboard_automatic_return: {params.usb_keyboard_automatic_return}")
print(f"usb_string_enable: {params.usb_string_enable}")
print(f"usb_fast_upload: {params.usb_fast_upload}")
# cmd: 136
# chip_working_mode: 128
# serial_comm_mode: 128
# serial_comm_address: 0
# serial_comm_baud_rate: 9600
# serial_comm_packet_interval: 3
# usb_vid: 6790
# usb_pid: 57641
# usb_keyboard_upload_interval: 0
# usb_keyboard_release_delay: 1
# usb_keyboard_automatic_return: 0
# usb_string_enable: 0
# usb_fast_upload: 0

ser.close()
```

## License

This project is licensed under the terms of the MIT license.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact

If you want to contact me you can reach me at pradish@sandbox.com.np.
