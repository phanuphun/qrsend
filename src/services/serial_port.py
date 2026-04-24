import serial

def writeToSerial(port: str, data: str, baud_rate: int = 9600):
    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        ser.write((data + '\n').encode('utf-8'))
        ser.close()
        print(f"ส่งข้อมูลไปที่ {port}: {data}")
    except serial.SerialException as e:
        print(f"เปิด {port} ไม่ได้: {e}")