import cv2
import time

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

def scanFrame() -> str | None:
    """อ่าน 1 frame และ return QR data หรือ None ถ้าไม่เจอ"""
    ret, frame = cap.read()
    if not ret:
        time.sleep(0.1)
        return None

    cv2.imshow("QR Scanner", frame)
    cv2.waitKey(1)

    data, _, _ = detector.detectAndDecode(frame)
    return data if data else None

def releaseCamera():
    cap.release()
    cv2.destroyAllWindows()
