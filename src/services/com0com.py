import subprocess
import ctypes
import sys
import os
import tempfile
import time

SETUPC_PATH = r"C:\Program Files (x86)\com0com\setupc.exe"
SETUPC_DIR  = r"C:\Program Files (x86)\com0com"

def isAdmin():
    return ctypes.windll.shell32.IsUserAnAdmin()

def installPair(port_a: str, port_b: str, emu_br: bool = False):
    """สร้าง virtual port pair ใหม่ เช่น installPair("COM5", "COM6", emu_br=True)"""
    br = "EmuBR=yes" if emu_br else ""
    prms_a = f"PortName={port_a},{br}" if br else f"PortName={port_a}"
    prms_b = f"PortName={port_b},{br}" if br else f"PortName={port_b}"
    args_str = f'install {prms_a} {prms_b}'

    if isAdmin():
        result = subprocess.run(
            [SETUPC_PATH, "install", prms_a, prms_b],
            capture_output=True, text=True, cwd=SETUPC_DIR
        )
        print(result.stdout or f"สร้าง pair {port_a} ↔ {port_b} เรียบร้อย")
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", SETUPC_PATH,
            args_str,
            SETUPC_DIR, 0
        )
        time.sleep(2.0)
        print(f"สร้าง pair {port_a} ↔ {port_b} เรียบร้อย (ต้องการ admin)")

def changePortName(port_id: str, port_name: str):
    """เปลี่ยนชื่อ port เช่น changePortName("CNCA0", "COM9")"""
    args_str = f'change {port_id} PortName={port_name}'

    if isAdmin():
        result = subprocess.run(
            [SETUPC_PATH, "change", port_id, f"PortName={port_name}"],
            capture_output=True, text=True, cwd=SETUPC_DIR
        )
        print(result.stdout or f"เปลี่ยน {port_id} → {port_name} เรียบร้อย")
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", SETUPC_PATH,
            args_str,
            SETUPC_DIR, 0  # SW_HIDE
        )
        time.sleep(1.5)
        print(f"เปลี่ยน {port_id} → {port_name} เรียบร้อย (ต้องการ admin)")

def listPorts():
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    tmp.close()

    if isAdmin():
        # รันตรงๆ ได้เลย
        subprocess.run(
            [SETUPC_PATH, "--output", tmp.name, "list"],
            capture_output=True, cwd=SETUPC_DIR
        )
    else:
        # ขอ elevation แบบ silent — เขียน output ลงไฟล์
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", SETUPC_PATH,
            f'--output "{tmp.name}" list',
            SETUPC_DIR, 0   # ← 0 = ซ่อน window
        )
        time.sleep(1.5)  # รอให้รันเสร็จ

    # อ่านจากไฟล์
    with open(tmp.name, "r") as f:
        output = f.read()

    os.unlink(tmp.name)  # ลบไฟล์ temp
    print(output)
    return output