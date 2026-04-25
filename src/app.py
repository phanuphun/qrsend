# app.py
import sys
import os

# Fix for PyInstaller: ensure 'services' package is findable at runtime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import argparse
import time
from services.camera import scanFrame, releaseCamera, initCamera, openCamera
from services.serial_port import writeToSerial
from services.com0com import listPorts, changePortName, installPair
from services.config import getCameraIndex, setCameraIndex, getCom0comPath, setCom0comPath

SCAN_COOLDOWN = 2.0  # วินาที — ป้องกันอ่าน QR เดิมซ้ำ

def main():
    parser = argparse.ArgumentParser(description="QR Serial Port Simulator")
    subparsers = parser.add_subparsers(dest="command")

    # คำสั่ง: scan
    scan_parser = subparsers.add_parser("scan", help="สแกน QR แล้วส่งเข้า serial port (วนซ้ำจนกว่าจะกด q/ESC)")
    scan_parser.add_argument("--port", type=str, required=True, help="COM port เช่น COM7")
    scan_parser.add_argument("--baud", type=int, default=9600, help="Baud rate (default: 9600)")

    # คำสั่ง: send
    send_parser = subparsers.add_parser("send", help="ส่งข้อมูลตรงๆ เข้า serial port")
    send_parser.add_argument("--port", type=str, required=True, help="COM port เช่น COM7")
    send_parser.add_argument("--data", type=str, required=True, help="ข้อมูลที่ต้องการส่ง")
    send_parser.add_argument("--baud", type=int, default=9600, help="Baud rate (default: 9600)")

    # คำสั่ง: list-ports
    subparsers.add_parser("list-ports", help="แสดง COM ports ที่มีอยู่ (สำหรับ Windows)")

    # คำสั่ง: install-pair
    install_parser = subparsers.add_parser("install-pair", help="สร้าง virtual COM port pair ใหม่")
    install_parser.add_argument("--port-a", type=str, required=True, help="ชื่อ port ฝั่ง A เช่น COM5")
    install_parser.add_argument("--port-b", type=str, required=True, help="ชื่อ port ฝั่ง B เช่น COM6")
    install_parser.add_argument("--emubr", action="store_true", help="เปิด Baud Rate emulation (ใช้เมื่อต้องการ timing จริง เช่น 9600)")

    # คำสั่ง: change-port
    change_parser = subparsers.add_parser("change-port", help="ตั้งชื่อ COM port เช่น CNCA0 → COM9")
    change_parser.add_argument("--id", type=str, required=True, help="Port identifier เช่น CNCA0 หรือ CNCB0")
    change_parser.add_argument("--name", type=str, required=True, help="ชื่อ COM port เช่น COM9")

    # คำสั่ง: set-camera
    set_camera_parser = subparsers.add_parser("set-camera", help="ตั้งค่า camera index ที่จะใช้ (default: 0)")
    set_camera_parser.add_argument("--index", type=int, required=True, help="Camera index เช่น 0, 1, 2")

    # คำสั่ง: open-camera
    open_camera_parser = subparsers.add_parser("open-camera", help="เปิดกล้องเพื่อทดสอบ (กด q หรือ ESC เพื่อปิด)")
    open_camera_parser.add_argument("--index", type=int, default=None, help="Camera index (default: ใช้ค่าที่ set-camera กำหนดไว้)")

    # คำสั่ง: set-com0com
    set_com0com_parser = subparsers.add_parser("set-com0com", help="ตั้งค่า path ของ setupc.exe")
    set_com0com_parser.add_argument("--path", type=str, required=True, help=r"เช่น C:\tools\com0com\setupc.exe")

    # คำสั่ง: get-com0com
    subparsers.add_parser("get-com0com", help="แสดง path ของ setupc.exe ที่ตั้งค่าไว้")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    if args.command == "scan":
        camera_index = getCameraIndex()
        initCamera(camera_index)
        print(f"QR Scanner เริ่มทำงาน... (camera index: {camera_index}) (q/ESC เพื่อหยุด)")
        last_data = ""
        last_time  = 0.0
        try:
            while True:
                qrData, quit_req = scanFrame()

                if quit_req:
                    print("\nหยุดการทำงาน")
                    break

                if not qrData:
                    continue

                now = time.time()
                if qrData == last_data and (now - last_time) < SCAN_COOLDOWN:
                    continue

                print(f"QR: {qrData}")
                writeToSerial(args.port, qrData, args.baud)

                last_data = qrData
                last_time  = now

        except KeyboardInterrupt:
            print("\nหยุดการทำงาน")
        finally:
            releaseCamera()

    elif args.command == "send":
        writeToSerial(args.port, args.data, args.baud)

    elif args.command == "list-ports":
        listPorts()

    elif args.command == "install-pair":
        installPair(args.port_a, args.port_b, emu_br=args.emubr)

    elif args.command == "change-port":
        changePortName(args.id, args.name)

    elif args.command == "set-camera":
        setCameraIndex(args.index)

    elif args.command == "open-camera":
        index = args.index if args.index is not None else getCameraIndex()
        openCamera(index)

    elif args.command == "set-com0com":
        setCom0comPath(args.path)

    elif args.command == "get-com0com":
        print(f"com0com path: {getCom0comPath()}")

if __name__ == "__main__":
    main()
