import cv2
import time

cap = None
detector = cv2.QRCodeDetector()


def initCamera(index: int = 0):
    """เปิดกล้องตาม index ที่กำหนด"""
    global cap
    cap = cv2.VideoCapture(index)


def openCamera(index: int = 0):
    """เปิดกล้องเพื่อทดสอบ — กด q หรือ ESC เพื่อปิด"""
    test_cap = cv2.VideoCapture(index)
    if not test_cap.isOpened():
        print(f"ไม่สามารถเปิดกล้อง index {index} ได้")
        return

    print(f"เปิดกล้อง index {index} — กด q หรือ ESC เพื่อปิด")
    while True:
        ret, frame = test_cap.read()
        if not ret:
            print("อ่าน frame ไม่ได้")
            break

        cv2.imshow(f"Camera {index} — Test", frame)
        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), 27):  # q หรือ ESC
            break

    test_cap.release()
    cv2.destroyAllWindows()
    print("ปิดกล้องแล้ว")


def scanFrame() -> tuple[str | None, bool]:
    """อ่าน 1 frame — return (qr_data, quit_requested)
    quit_requested = True เมื่อผู้ใช้กด q หรือ ESC"""
    ret, frame = cap.read()
    if not ret:
        time.sleep(0.1)
        return None, False

    cv2.imshow("QR Scanner", frame)
    key = cv2.waitKey(1) & 0xFF
    quit_requested = key in (ord("q"), 27)  # q หรือ ESC

    data, _, _ = detector.detectAndDecode(frame)
    return (data if data else None), quit_requested


def releaseCamera():
    cap.release()
    cv2.destroyAllWindows()
