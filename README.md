# QR Serial Port Simulator

A Windows utility that reads QR codes via webcam and forwards the data through a virtual serial port. Designed for systems that expect barcode/QR input over a COM port interface.

---

## Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| [com0com](https://sourceforge.net/projects/com0com/) | 2.2.2.0 (signed) | Must use the digitally signed build — unsigned drivers will not function on Windows 10/11 |

---

## Installation

### 1. Install com0com

Download and install the **digitally signed** com0com driver (v2.2.2.0). Unsigned versions will show warning icons in Device Manager and COM ports will be inaccessible.

### 2. Clone the repository

```bash
git clone https://github.com/your-username/qr-serial-port-simulator.git
cd qr-serial-port-simulator
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a virtual COM port pair

Run the following command to create a virtual port pair (e.g. COM5 ↔ COM6). This requires Administrator privileges — a UAC prompt will appear if not already elevated.

```bash
python run.py install-pair --port-a COM5 --port-b COM6
```

Verify the ports were created:

```bash
python run.py list-ports
```

### 5. (Optional) Configure com0com path

If com0com is installed in a non-default location, set the path to `setupc.exe`:

```bash
python run.py set-com0com --path "C:\tools\com0com\setupc.exe"
```

### 6. (Optional) Configure camera

Test that your camera opens correctly, then set the index if needed:

```bash
python run.py open-camera
python run.py set-camera --index 1
```

---

## Quick Start

```bash
python run.py scan --port COM5
```

Point a QR code at the webcam. The decoded data will be sent to `COM5` and can be read by any application listening on the paired port (`COM6`).

Press **q** or **ESC** on the camera window to stop.

---

## Building as an Executable

Install PyInstaller and build:

```bash
pip install pyinstaller
pyinstaller --onefile --collect-all cv2 --paths src --name qrsend src/app.py
```

The executable will be output to `dist/qrsend.exe`.

To use `qrsend` from any terminal, add the `dist/` folder to your system PATH.

---

## Commands

### Scanning & Sending
```
scan --port <COM> [--baud <rate>]          Scan QR continuously, press q/ESC to stop
send --port <COM> --data <string>          Send a string directly to a COM port
```

### Virtual COM Port
```
list-ports                                 List all virtual COM ports
install-pair --port-a <COM> --port-b <COM> [--emubr]   Create a new port pair (requires Admin)
change-port --id <CNCA0> --name <COM>      Rename a port identifier to a COM name
```

### Camera
```
open-camera [--index <n>]                  Open camera preview to test (q/ESC to close)
set-camera --index <n>                     Set default camera index (saved to config.json)
```

### com0com Path
```
get-com0com                                Show current path to setupc.exe
set-com0com --path <path>                  Set path to setupc.exe (saved to config.json)
```

---