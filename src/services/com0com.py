import subprocess
import ctypes
import os
import tempfile
import time

from services.config import getCom0comPath


def _getPaths() -> tuple[str, str]:
    """Return (setupc_path, setupc_dir) จาก config"""
    setupc_path = getCom0comPath()
    setupc_dir  = os.path.dirname(setupc_path)
    return setupc_path, setupc_dir


def isAdmin():
    return ctypes.windll.shell32.IsUserAnAdmin()


def installPair(port_a: str, port_b: str, emu_br: bool = False):
    """สร้าง virtual port pair ใหม่ เช่น installPair("COM5", "COM6", emu_br=True)"""
    setupc_path, setupc_dir = _getPaths()
    br = "EmuBR=yes" if emu_br else ""
    prms_a = f"PortName={port_a},{br}" if br else f"PortName={port_a}"
    prms_b = f"PortName={port_b},{br}" if br else f"PortName={port_b}"
    args_str = f'install {prms_a} {prms_b}'

    if isAdmin():
        result = subprocess.run(
            [setupc_path, "install", prms_a, prms_b],
            capture_output=True, text=True, cwd=setupc_dir
        )
        print(result.stdout or f"สร้าง pair {port_a} ↔ {port_b} เรียบร้อย")
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", setupc_path,
            args_str,
            setupc_dir, 0
        )
        time.sleep(2.0)
        print(f"สร้าง pair {port_a} ↔ {port_b} เรียบร้อย (ต้องการ admin)")


def changePortName(port_id: str, port_name: str):
    """เปลี่ยนชื่อ port เช่น changePortName("CNCA0", "COM9")"""
    setupc_path, setupc_dir = _getPaths()
    args_str = f'change {port_id} PortName={port_name}'

    if isAdmin():
        result = subprocess.run(
            [setupc_path, "change", port_id, f"PortName={port_name}"],
            capture_output=True, text=True, cwd=setupc_dir
        )
        print(result.stdout or f"เปลี่ยน {port_id} → {port_name} เรียบร้อย")
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", setupc_path,
            args_str,
            setupc_dir, 0
        )
        time.sleep(1.5)
        print(f"เปลี่ยน {port_id} → {port_name} เรียบร้อย (ต้องการ admin)")


def listPorts():
    setupc_path, setupc_dir = _getPaths()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    tmp.close()

    if isAdmin():
        subprocess.run(
            [setupc_path, "--output", tmp.name, "list"],
            capture_output=True, cwd=setupc_dir
        )
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", setupc_path,
            f'--output "{tmp.name}" list',
            setupc_dir, 0
        )
        time.sleep(1.5)

    with open(tmp.name, "r") as f:
        output = f.read()

    os.unlink(tmp.name)
    print(output)
    return output
