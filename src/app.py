# app.py
import argparse
from services.camera import openCamera
from services.serial_port import writeToSerial
from services.com0com import listPorts, changePortName, installPair

def main():
    parser = argparse.ArgumentParser(description="QR Serial Port Simulator")
    subparsers = parser.add_subparsers(dest="command")

    # คำสั่ง: scan
    scan_parser = subparsers.add_parser("scan", help="สแกน QR แล้วส่งเข้า serial port")
    scan_parser.add_argument("--port", type=str, required=True, help="COM port เช่น COM9")
    scan_parser.add_argument("--baud", type=int, default=9600, help="Baud rate (default: 9600)")

    # คำสั่ง: send
    send_parser = subparsers.add_parser("send", help="ส่งข้อมูลตรงๆ เข้า serial port")
    send_parser.add_argument("--port", type=str, required=True, help="COM port เช่น COM9")
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

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    if args.command == "scan":
        print(f"เปิดกล้อง... กำลังรอ QR code")
        qrData = openCamera()
        if qrData:
            print(f"QR: {qrData}")
            writeToSerial(args.port, qrData, args.baud)

    elif args.command == "send":
        writeToSerial(args.port, args.data, args.baud)

    elif args.command == "list-ports":
        listPorts()

    elif args.command == "install-pair":
        installPair(args.port_a, args.port_b, emu_br=args.emubr)

    elif args.command == "change-port":
        changePortName(args.id, args.name)

if __name__ == "__main__":
    main()