# CLI Command Reference

All commands can be run with `python run.py <command>` or `qrsend <command>` (if built as executable).

---

## scan

Start the QR scanner. Reads QR codes continuously from the webcam and sends each result to a COM port. Press **q** or **ESC** on the camera window to stop.

```
qrsend scan --port <COM> [--baud <rate>]
```

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--port` | ✅ | — | Target COM port, e.g. `COM5` |
| `--baud` | — | `9600` | Baud rate |

**Example**
```bash
qrsend scan --port COM5
qrsend scan --port COM5 --baud 115200
```

---

## send

Send a string directly to a COM port without scanning.

```
qrsend send --port <COM> --data <string> [--baud <rate>]
```

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--port` | ✅ | — | Target COM port, e.g. `COM5` |
| `--data` | ✅ | — | String to send |
| `--baud` | — | `9600` | Baud rate |

**Example**
```bash
qrsend send --port COM5 --data "Hello"
qrsend send --port COM5 --data "ABC123" --baud 115200
```

---

## list-ports

List all virtual COM ports currently created by com0com.

```
qrsend list-ports
```

---

## install-pair

Create a new virtual COM port pair. Requires Administrator privileges — a UAC prompt will appear if not already elevated.

```
qrsend install-pair --port-a <COM> --port-b <COM> [--emubr]
```

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--port-a` | ✅ | — | Port A name, e.g. `COM5` |
| `--port-b` | ✅ | — | Port B name, e.g. `COM6` |
| `--emubr` | — | off | Enable baud rate emulation for accurate timing |

**Example**
```bash
qrsend install-pair --port-a COM5 --port-b COM6
qrsend install-pair --port-a COM5 --port-b COM6 --emubr
```

---

## change-port

Rename a com0com port identifier (e.g. `CNCA0`) to a friendlier COM port name (e.g. `COM9`). Requires Administrator privileges.

```
qrsend change-port --id <identifier> --name <COM>
```

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--id` | ✅ | — | Port identifier from com0com, e.g. `CNCA0`, `CNCB0` |
| `--name` | ✅ | — | New COM port name, e.g. `COM9` |

**Example**
```bash
qrsend change-port --id CNCA0 --name COM5
qrsend change-port --id CNCB0 --name COM6
```

---

## open-camera

Open a camera preview window for testing. Press **q** or **ESC** to close.

```
qrsend open-camera [--index <n>]
```

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--index` | — | saved value | Camera index to open. If omitted, uses the value set by `set-camera` |

**Example**
```bash
qrsend open-camera
qrsend open-camera --index 1
```

---

## set-camera

Set the default camera index used by the `scan` command. The value is saved to `config.json` and persists across sessions.

```
qrsend set-camera --index <n>
```

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--index` | ✅ | — | Camera index — `0` is the first camera, `1` is the second, etc. |

**Example**
```bash
qrsend set-camera --index 0
qrsend set-camera --index 1
```

---

## get-com0com

Display the currently configured path to `setupc.exe`.

```
qrsend get-com0com
```

---

## set-com0com

Set the path to `setupc.exe`. Use this if com0com is installed in a non-default location. The value is saved to `config.json`.

```
qrsend set-com0com --path <path>
```

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--path` | ✅ | — | Full path to `setupc.exe` |

**Example**
```bash
qrsend set-com0com --path "C:\tools\com0com\setupc.exe"
```

---

## Summary

| Command | Description |
|---------|-------------|
| `scan` | Start QR scanner → send to serial port |
| `send` | Send string directly to serial port |
| `list-ports` | List all virtual COM ports |
| `install-pair` | Create a new virtual COM port pair |
| `change-port` | Rename a port identifier to a COM name |
| `open-camera` | Open camera preview for testing |
| `set-camera` | Set default camera index |
| `get-com0com` | Show path to setupc.exe |
| `set-com0com` | Set path to setupc.exe |
