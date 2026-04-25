# QR Serial Port Simulator

A Windows utility that reads QR codes via webcam and forwards the data through a virtual serial port. Designed for systems that expect barcode/QR input over a COM port interface.

---

## Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| [Python](https://www.python.org/downloads/) | 3.12+ | |
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
pyinstaller --onefile --collect-all cv2 --name qrsend src/app.py
```

The executable will be output to `dist/qrsend.exe`.

To use `qrsend` from any terminal, add the `dist/` folder to your system PATH.

---

## Commands

### Scanning & Sending

| Command | Description |
|---|---|
| `scan --port <COM> [--baud <rate>]` | Start QR scanner. Reads continuously until **q** or **ESC** is pressed. Sends each scan to the specified COM port. |
| `send --port <COM> --data <string> [--baud <rate>]` | Send a string directly to a COM port without scanning. |

**Options:**

| Option | Default | Description |
|---|---|---|
| `--port` | *(required)* | Target COM port, e.g. `COM5` |
| `--data` | *(required for send)* | Data string to send |
| `--baud` | `9600` | Baud rate |

---

### Virtual COM Port Management

| Command | Description |
|---|---|
| `list-ports` | List all virtual COM ports created by com0com. |
| `install-pair --port-a <COM> --port-b <COM> [--emubr]` | Create a new virtual COM port pair. Requires Administrator privileges. |
| `change-port --id <id> --name <COM>` | Rename a port identifier (e.g. `CNCA0`) to a COM port name (e.g. `COM9`). |

**Options:**

| Option | Default | Description |
|---|---|---|
| `--port-a` | *(required)* | Port A name, e.g. `COM5` |
| `--port-b` | *(required)* | Port B name, e.g. `COM6` |
| `--emubr` | `false` | Enable baud rate emulation for accurate timing |
| `--id` | *(required)* | Port identifier, e.g. `CNCA0` or `CNCB0` |
| `--name` | *(required)* | New COM port name, e.g. `COM9` |

---

### Camera Configuration

| Command | Description |
|---|---|
| `open-camera [--index <n>]` | Open the camera for testing. Press **q** or **ESC** to close. |
| `set-camera --index <n>` | Set the default camera index used by the `scan` command. Saved to `config.json`. |

**Options:**

| Option | Default | Description |
|---|---|---|
| `--index` | `0` (or saved value) | Camera index — `0` is the first camera, `1` is the second, etc. |

---

### com0com Configuration

| Command | Description |
|---|---|
| `set-com0com --path <path>` | Set the path to `setupc.exe`. Use this if com0com is installed in a non-default location. Saved to `config.json`. |
| `get-com0com` | Display the currently configured path to `setupc.exe`. |

**Options:**

| Option | Default | Description |
|---|---|---|
| `--path` | *(required)* | Full path to `setupc.exe`, e.g. `C:\tools\com0com\setupc.exe` |

---

## Configuration

Settings are persisted in `config.json` at the project root. The file is created automatically on first use.

| Key | Default | Description |
|---|---|---|
| `camera_index` | `0` | Camera index used by the `scan` command |
| `com0com_path` | `C:\Program Files (x86)\com0com\setupc.exe` | Path to `setupc.exe` |

---