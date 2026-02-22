import warnings
warnings.filterwarnings("ignore")   # suppress YOLO / torch warnings

import cv2
import torch
# Load YOLOv5 model
print("Loading YOLOv5 model...")
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Initialize QR Code Detector
qr_detector = cv2.QRCodeDetector()

# Open Camera
cap = cv2.VideoCapture(0)

print("Camera started")
print("Show a CLEAR QR code to the camera")
print("Press 'q' to quit")

# Main Loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read camera frame", flush=True)
        break

    # YOLO Object Detection (STEP 2)
    with torch.no_grad():        # prevents memory crash
        results = model(frame)
        results.render()

    # QR Detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    data, bbox, _ = qr_detector.detectAndDecode(gray)

    # Draw QR bounding box
    if bbox is not None:
        bbox = bbox.astype(int)
        for i in range(len(bbox[0])):
            pt1 = tuple(bbox[0][i])
            pt2 = tuple(bbox[0][(i + 1) % len(bbox[0])])
            cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

    # Print QR data to terminal
    if data:
        print("Scanned QR:", data, flush=True)

        cv2.putText(
            frame,
            data,
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    # Display Output
    cv2.imshow("YOLO + QR Inventory System", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("Program stopped", flush=True)