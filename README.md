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

ser = Serial("COM3", 9600, timeout=1)

keyboard.press_and_release(ser, "a", modifier="ctrl")
keyboard.write(ser, "Hello World\n")
keyboard.write(ser, "abcdefghijklmnopqrstuvwxyz\n")
keyboard.write(ser, "ABCDEFGHIJKLMNOPQRSTUVWXYZ\n")
keyboard.write(ser, "0123456789\n")
keyboard.write(ser, "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~\n")

mouse.move(ser, x=500, y=500)
mouse.move(ser, x=50, y=50, relative=True)
mouse.click(ser, button="left")

ser.close()
```

## License

This project is licensed under the terms of the MIT license.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact

If you want to contact me you can reach me at pradish@sandbox.com.np.
