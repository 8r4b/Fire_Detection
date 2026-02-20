import cv2
from ultralytics import YOLO

# Load your trained YOLO model
model = YOLO("C:/Users/msi-pc/OneDrive/سطح المكتب/best.pt")


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # Run YOLO detection
    results = model(frame)

    # Draw bounding boxes and labels
    annotated_frame = results[0].plot()

    cv2.imshow("Fire Detection", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
