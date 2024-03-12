# ch9329

Python module to control ch9329

## Installation

You can install the package via pip:

```bash
pip install ch9329
```

## Usage

```python
import ch9329
from serial import Serial

ser = Serial("COM3", 9600, timeout=1)

"""
ctrl:
    control_left
    shift_left
    alt_left
    gui_left
    control_right
    shift_right
    alt_right
    gui_right

"""

ch9329.keyboard.press_and_release(ser = ser, key="a", ctrl="control_left")
ch9329.keyboard.write(ser = ser, text="HEllo@World;")

"""
button:
    ST
    NU - NULL for releasing buttons
    LE - Left button
    RI - Right button
    CE
"""

ch9329.mouse.move(ser = ser, x=100, y=300)
ch9329.mouse.press(ser = ser, button="LE")
ch9329.mouse.move(ser = ser, x=1000, y=1000)

ser.close()

```

## License

This project is licensed under the terms of the MIT license.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact

If you want to contact me you can reach me at pradish@sandbox.com.np.
