import cv2
import requests
import time

cap = cv2.VideoCapture(0)

detector = cv2.QRCodeDetector()

last_scanned = ""
last_time = 0

print("Scanner started...")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    data, bbox, _ = detector.detectAndDecode(frame)

    if data:

        current_time = time.time()

        if data != last_scanned or (current_time - last_time) > 3:

            print("Scanned:", data)

            try:
                requests.post(
                    "http://127.0.0.1:5000/add_item",
                    json={"item_id": data}
                )
            except:
                print("Backend not running")

            last_scanned = data
            last_time = current_time

        if bbox is not None:
            for i in range(len(bbox)):
                pt1 = tuple(bbox[i][0].astype(int))
                pt2 = tuple(bbox[(i+1) % len(bbox)][0].astype(int))
                cv2.line(frame, pt1, pt2, (0,255,0), 2)

    cv2.imshow("QR Scanner", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()