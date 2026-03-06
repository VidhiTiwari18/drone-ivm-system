import cv2
import requests
from pyzbar.pyzbar import decode

# Open camera
cap = cv2.VideoCapture(0)

print("Scanner started...")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Detect barcode
    barcodes = decode(frame)

    for barcode in barcodes:

        # Convert barcode bytes to string
        barcode_data = barcode.data.decode("utf-8")

        print("Scanned:", barcode_data)

        # Send data to Flask backend
        try:
            requests.post(
                "http://127.0.0.1:5000/add_item",
                json={"item_id": barcode_data}
            )
        except:
            print("Backend not running")

        # Draw rectangle around barcode
        x, y, w, h = barcode.rect
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        cv2.putText(
            frame,
            barcode_data,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

    cv2.imshow("Barcode Scanner", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()