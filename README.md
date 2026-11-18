# PBN-Control

## Background
This repository contains code for controlling a PBN (programmable bevel-tip needle) using Dynamixel motors. The code is written in Python and uses the Dynamixel SDK to communicate with the motors. It also includes:

- Arduino sketches and Python readers for PMW3360 optical encoders ("opten"), used to measure segment displacement independently of the motors.
- Data logging to CSV and analysis notebooks.
- Webcam recording with point tracking (`cam_stream.ipynb`).

## Repository Structure

| Path | Description |
| --- | --- |
| `sync_dual.py`, `sync_quad.py` | Motor driver modules. Define the port/ID settings and the `Dynamixel` (2 motors) / `DynamixelQuad` (4 motors) classes: torque, operating mode, position, velocity, current limit, profile velocity/acceleration, LED, voltage/current/temperature readout, plus `set_dualpos`/`set_dualvel` and `set_quadpos`/`set_quadvel`. |
| `blockcon_dual.py`, `blockcon_quad.py` | Scripted ("block") control: demo sequences for velocity, profile position and current-based position control. Edit the demo blocks between the "DONT CHANGE" sections. |
| `guicon_dual.py`, `guicon_quad.py` | PyQt5 GUIs for manual velocity control by keyboard or gamepad, showing position, voltage, current and temperature per motor. |
| `guicon_opten.py` | Dual-motor GUI that also reads both optical encoders, plots motor vs. encoder positions live (pyqtgraph) and exports data to `exports/stream_data_<datetime>.csv`. |
| `opten_lib.py` | Optical encoder serial interface: `SerialReader` (burst or camera mode) and `OpticalDuo` (connects to both encoders). |
| `opten_pos.py` | Scripted test: moves both motors back and forth in extended position mode while logging motor position/current and encoder positions to `exports/stream_<timestamp>.csv`, then plots them. |
| `opten_camplot.py` | Like `opten_pos.py` but with the encoders in camera mode; logs 36x36 sensor images to `exports/camstream_<timestamp>.csv`. |
| `opten_ctrl.py`, `sync_template.py` | Empty templates that initialise (and close) the motors, and the encoders for `opten_ctrl.py`. |
| `cam_stream.ipynb` | Webcam streaming (camera index 1, 1920x1080 at 60 fps). Lets you select a feature point, tracks it with Lucas-Kanade optical flow and saves `output_<timestamp>.avi` and `output_<timestamp>.csv`. |
| `opten_camvid.ipynb` | Converts a `camstream_*.csv` from `opten_camplot.py` into an MP4 video of both encoder images. |
| `data_reader.ipynb`, `data_reader copy.ipynb` | Plot motor vs. encoder position, velocity and difference from logged CSVs. |
| `arduino/` | Arduino sketches for the PMW3360: `PMW3360DM_Burst` (motion burst, prints X/Y motion deltas per line) and `PMW3360DM_Camera` (prints 36x36 frame images). These are the versions `opten_lib.py` expects. |
| `opten/installation/` | `AdvMouse` Arduino library, plus older copies of the Burst/Camera sketches (`PMW3360DM-Burst`, `PMW3360DM-Camera`). |
| `opten/` | Early standalone encoder scripts: `read_*.py` (print serial output, quit with `q`) and `plot_*.py` (PyQt5/pyqtgraph live plots; `plot_camera.py` saves images to `opten/camera/`). |
| `opten/camera/` | Saved optical encoder images. |
| `python/` | Bundled copy of the ROBOTIS DynamixelSDK Python package (v3.7.31) with its example tests. |
| `tests/` | Development tests: single-motor demos (`test_demo.py`, `test_pos.py`), gamepad tests (`test_gamepad.py`, `test_gamebuttons.py`), single encoder test (`opten_one.py`), a PyQt switch widget (`test_qt.py`) and `test_library.ipynb`. |
| `exports/` | Logged CSV data (`Time`, motor and encoder positions). |
| `control_table.txt` | Dynamixel control table addresses (Protocol 2.0). |

## Installation

### Python dependencies
From the imports in the code:

- `dynamixel_sdk` (see below; it requires `pyserial`)
- `pyserial`
- `PyQt5` (including QtMultimedia)
- `pyqtgraph`
- `inputs` (gamepad)
- `numpy`, `pandas`, `matplotlib`
- `opencv-python` (notebooks)
- `keyboard` (only `opten/read_*.py`)

```
pip install pyserial PyQt5 pyqtgraph inputs numpy pandas matplotlib opencv-python keyboard
```

### Motor library (DynamixelSDK)
Please follow the instructions here to install DynamixelSDK for Windows Python:
- https://github.com/ROBOTIS-GIT/DynamixelSDK
- https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/library_setup/python_windows/#python-windows

A copy of the SDK is also in `python/` and can be installed with `pip install ./python`.

### Optical encoders
The optical encoders used are the PMW3360 Motion Sensor from Joe's Sensors and Sundry, available from https://www.tindie.com/products/citizenjoe/pmw3360-motion-sensor/.

The optical encoders are controlled by an Arduino Uno over SPI, using code based on https://github.com/SunjunKim/PMW3360_Arduino. Copy `opten/installation/AdvMouse/` to your Arduino library folder. Then load a sketch from `arduino/` onto each Arduino using the Arduino IDE:

- `arduino/PMW3360DM_Burst/` for position tracking (used by `guicon_opten.py`, `opten_pos.py`).
- `arduino/PMW3360DM_Camera/` for sensor images (used by `opten_camplot.py`).

`opten_lib.py` waits for the `DPI set to` and `Optical Chip Initialised` messages printed by the `arduino/` sketches; the older sketches in `opten/installation/` print different messages and will not initialise with it.

The Python side uses PySerial to communicate with the Arduinos.

## Hardware Setup

### Motor IDs
Please change the motor ID and reverse mode (if needed) using Dynamixel Wizard 2.0. Install from https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/

Looking from the rear end of the PBN:
- ID 1: Top segment (set to reverse mode, Address 10 = 1)
- ID 2: Left segment (set to reverse mode, Address 10 = 1)
- ID 3: Right segment
- ID 4: Bottom segment

ID mapping in code:
- `sync_dual.py`: `DXL1_ID = 2`, `DXL2_ID = 3` (left and right).
- `sync_quad.py`: `DXL1_ID = 2`, `DXL2_ID = 3`, `DXL3_ID = 1`, `DXL4_ID = 4`.

### Ports and settings (as configured in code)

| Device | Setting | Where |
| --- | --- | --- |
| Dynamixel controller | `DEVICENAME = 'COM3'`, 57600 baud, Protocol 2.0 | `sync_dual.py`, `sync_quad.py` |
| Optical encoder 1 | `COM5`, 9600 baud | `opten_lib.py` (`OPT1`) |
| Optical encoder 2 | `COM6`, 9600 baud, X axis flipped in burst mode | `opten_lib.py` (`OPT2`) |
| Arduino sketches | CPI 12000, SPI slave select on pin 10 | `arduino/*/*.ino` |
| Webcam | `cv2.VideoCapture(1)` | `cam_stream.ipynb` |

Change these to match your machine. Some scripts in `opten/` and `tests/` hard-code other COM ports (e.g. `COM4`). Make sure no other software (e.g. Dynamixel Wizard or the Arduino serial monitor) is holding the port.

Operating modes available via `set_mode`: `"vel"` (velocity), `"pos"` (position), `"extpos"` (extended position), `"curpos"` (current-based position), `"cur"` (current), `"pwm"`. Per the comments in `blockcon_*.py`, a velocity of 3.33 units corresponds to 1 mm/s.

## Usage
Run the scripts from the repository root (they import `sync_dual`/`sync_quad`/`opten_lib` from there, and write to `./exports`).

### Scripted control
```
python blockcon_dual.py
python blockcon_quad.py
```
Edit the demo section of the script to set your motion sequence. Torque is enabled at the start and disabled at the end.

### GUI control
```
python guicon_dual.py
python guicon_quad.py
python guicon_opten.py
```
If a gamepad is connected, the left stick Y (`ABS_Y`) drives motor 1, the right stick Y (`ABS_RY`) drives motor 2, and Start/Select toggle their torque.

> **Note:** in `guicon_quad.py` the gamepad only drives motors 1 and 2, and on close only motors 1 and 2 have torque disabled. Motors 3 and 4 stay torqued until you toggle them off (U / I) or power down.

Keyboard controls (hold to move, release to stop; hold Shift to boost):

| GUI | Motor 1 | Motor 2 | Motor 3 | Motor 4 | Torque toggle | Speed / boost |
| --- | --- | --- | --- | --- | --- | --- |
| `guicon_dual.py` | Q / W | A / S | - | - | T, Y | 16, x3 |
| `guicon_quad.py` | E / R | D / F | Q / W | A / S | T, Y, U, I | 5, x5 |
| `guicon_opten.py` | Q / W | A / S | - | - | T, Y | 6, x5 |

In `guicon_opten.py`, R resets motor and encoder positions, M resets the time, and the "Export Data" button saves the logged data. Esc closes the GUIs.

### Optical encoder logging
```
python opten_lib.py      # connect, initialise and close both encoders
python opten_pos.py      # motor + encoder position test, saves CSV and plots
python opten_camplot.py  # encoder camera-mode logging
```

### Camera recording
Open `cam_stream.ipynb` in Jupyter. Run the tracking cell, enter the number of a detected point to track, and press `q` in the video window to stop recording.
