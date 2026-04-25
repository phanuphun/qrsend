# app.py
import argparse
import time
from services.camera import scanFrame, releaseCamera
from services.serial_port import writeToSerial
from services.com0com import listPorts, changePortName, installPair
from services.mqtt_client import publishMessage

SCAN_COOLDOWN = 2.0  # วินาที — ป้องกันอ่าน QR เดิมซ้ำ

def main():
    parser = argparse.ArgumentParser(description="QR Serial Port Simulator")
    subparsers = parser.add_subparsers(dest="command")

    # คำสั่ง: scan
    scan_parser = subparsers.add_parser("scan", help="สแกน QR แล้วส่งเข้า serial port (วนซ้ำจนกว่าจะกด Ctrl+C)")
    scan_parser.add_argument("--port", type=str, required=True, help="COM port เช่น COM7")
    scan_parser.add_argument("--baud", type=int, default=9600, help="Baud rate (default: 9600)")
    scan_parser.add_argument("--mqtt", action="store_true", help="Publish ข้อมูลไปยัง MQTT broker ด้วย")
    scan_parser.add_argument("--topic", type=str, default="qr/scan", help="MQTT topic (default: qr/scan)")
    scan_parser.add_argument("--mqtt-host", type=str, default="localhost", help="MQTT broker host (default: localhost)")
    scan_parser.add_argument("--mqtt-port", type=int, default=1883, help="MQTT broker port (default: 1883)")

    # คำสั่ง: send
    send_parser = subparsers.add_parser("send", help="ส่งข้อมูลตรงๆ เข้า serial port")
    send_parser.add_argument("--port", type=str, required=True, help="COM port เช่น COM7")
    send_parser.add_argument("--data", type=str, required=True, help="ข้อมูลที่ต้องการส่ง")
    send_parser.add_argument("--baud", type=int, default=9600, help="Baud rate (default: 9600)")
    send_parser.add_argument("--mqtt", action="store_true", help="Publish ข้อมูลไปยัง MQTT broker ด้วย")
    send_parser.add_argument("--topic", type=str, default="qr/scan", help="MQTT topic (default: qr/scan)")
    send_parser.add_argument("--mqtt-host", type=str, default="localhost", help="MQTT broker host (default: localhost)")
    send_parser.add_argument("--mqtt-port", type=int, default=1883, help="MQTT broker port (default: 1883)")

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
        print(f"QR Scanner เริ่มทำงาน... (Ctrl+C เพื่อหยุด)")
        last_data = ""
        last_time  = 0.0
        try:
            while True:
                qrData = scanFrame()
                if not qrData:
                    continue

                now = time.time()
                # ป้องกันอ่าน QR เดิมซ้ำภายใน cooldown
                if qrData == last_data and (now - last_time) < SCAN_COOLDOWN:
                    continue

                print(f"QR: {qrData}")
                writeToSerial(args.port, qrData, args.baud)
                if args.mqtt:
                    publishMessage(qrData, args.topic, args.mqtt_host, args.mqtt_port)

                last_data = qrData
                last_time  = now

        except KeyboardInterrupt:
            print("\nหยุดการทำงาน")
            releaseCamera()

    elif args.command == "send":
        writeToSerial(args.port, args.data, args.baud)
        if args.mqtt:
            publishMessage(args.data, args.topic, args.mqtt_host, args.mqtt_port)

    elif args.command == "list-ports":
        listPorts()

    elif args.command == "install-pair":
        installPair(args.port_a, args.port_b, emu_br=args.emubr)

    elif args.command == "change-port":
        changePortName(args.id, args.name)

if __name__ == "__main__":
    main()
