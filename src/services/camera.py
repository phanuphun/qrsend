import cv2
import time

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

def openCamera():
    print("QR Scanner รันอยู่เบื้องหลัง... (Ctrl+C เพื่อหยุด)")

    while True:
        ret, frame = cap.read()
        if not ret:
            time.sleep(0.1)
            continue


        cv2.imshow("Debug", frame)   # ← เพิ่มบรรทัดนี้
        cv2.waitKey(1)               # ← และบรรทัดนี้

        data, _, _ = detector.detectAndDecode(frame)

        if data:
            cap.release()
            cv2.destroyAllWindows()
            return data