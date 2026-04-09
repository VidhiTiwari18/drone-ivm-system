import cv2
import requests
import time

# try pyzbar
try:
    from pyzbar.pyzbar import decode
    use_pyzbar = True
    print("Using pyzbar")
except:
    use_pyzbar = False
    print("Using OpenCV QR")

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

last_data = ""
last_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    scanned_data = ""

    # ---------- pyzbar ----------
    if use_pyzbar:
        barcodes = decode(frame)

        for barcode in barcodes:
            scanned_data = barcode.data.decode("utf-8")

            x, y, w, h = barcode.rect
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    # ---------- OpenCV fallback ----------
    else:
        data, bbox, _ = detector.detectAndDecode(frame)

        if data:
            scanned_data = data

        if bbox is not None:
            for i in range(len(bbox)):
                pt1 = tuple(bbox[i][0].astype(int))
                pt2 = tuple(bbox[(i+1)%len(bbox)][0].astype(int))
                cv2.line(frame, pt1, pt2, (0,255,0), 2)

    # ---------- send to backend ----------
    if scanned_data:
        current_time = time.time()

        if scanned_data != last_data or (current_time - last_time) > 3:
            print("Scanned:", scanned_data)

            try:
                 response = requests.post(
                    "http://127.0.0.1:5000/add_item",
                    json={"item_id": scanned_data}
                )
                 print("Status:", response.status_code)
                 print("Response:", response.text)

            except Exception as e:
                print("Error:",e)

            last_data = scanned_data
            last_time = current_time

    cv2.imshow("Scanner", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()