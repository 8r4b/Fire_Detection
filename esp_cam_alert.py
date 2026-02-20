import cv2
from ultralytics import YOLO
import threading
import queue
import time
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage

# --------------------- Gmail Config ---------------------
SENDER_EMAIL = "mohamedalsaedi1999@gmail.com"
SENDER_PASSWORD = "oroj jcuk nkyo lhsp"  # Gmail App Password
RECIPIENT_EMAIL = "mohamedalsaedi1999@gmail.com"

ALERT_COOLDOWN = 10  # seconds
last_alert_time = 0

# --------------------- Fire Image Folder ---------------------
FIRE_FOLDER = "fire_detected"
os.makedirs(FIRE_FOLDER, exist_ok=True)

# --------------------- YOLO Model ---------------------
model = YOLO("C:/Users/msi-pc/OneDrive/سطح المكتب/best.pt")

# --------------------- ESP32 Stream ---------------------
stream_url = "http://192.168.1.1:81/stream"
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Cannot open ESP32 stream")
    exit()

cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Frame dimensions
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

scale_factor = 2.1
display_width = int(frame_width * scale_factor)
display_height = int(frame_height * scale_factor)

# --------------------- Queues & Threading ---------------------
frame_queue = queue.Queue(maxsize=2)
result_queue = queue.Queue(maxsize=1)
stop_event = threading.Event()

# --------------------- Gmail Alert Function ---------------------
def send_email_alert(subject, body, image_path):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg.set_content(body)

    with open(image_path, 'rb') as img:
        img_data = img.read()
        img_name = os.path.basename(image_path)
    msg.add_attachment(img_data, maintype='image', subtype='jpeg', filename=img_name)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
            print("Email alert sent successfully!")
    except Exception as e:
        print("Email error:", e)

# --------------------- Capture Frames ---------------------
def capture_frames():
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            continue
        try:
            frame_queue.put(frame, block=False)
        except queue.Full:
            pass

# --------------------- Process Frames ---------------------
def process_frames():
    global last_alert_time

    while not stop_event.is_set():
        try:
            frame = frame_queue.get(timeout=1)
            results = model(frame, imgsz=320, verbose=False)

            fire_detected = False
            fire_confidence = 0.0

            if results[0].boxes is not None:
                for box in results[0].boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])

                    # Fire class ID = 0
                    if cls_id == 0 and conf >= 0.4:
                        fire_detected = True
                        fire_confidence = conf
                        break

            annotated = results[0].plot()

            if fire_detected:
                now = time.time()
                if now - last_alert_time > ALERT_COOLDOWN:
                    # ---------- Save Image ----------
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    image_path = os.path.join(FIRE_FOLDER, f"fire_{timestamp}.jpg")
                    cv2.imwrite(image_path, annotated)

                    # ---------- Send Gmail Alert in a separate thread ----------
                    subject = "🔥 FIRE DETECTED!"
                    body = f"Confidence: {fire_confidence:.2f}\nSource: Drone Camera"
                    threading.Thread(target=send_email_alert, args=(subject, body, image_path), daemon=True).start()

                    last_alert_time = now

            try:
                result_queue.put(annotated, block=False)
            except queue.Full:
                pass

        except queue.Empty:
            continue

# --------------------- Start Threads ---------------------
capture_thread = threading.Thread(target=capture_frames, daemon=True)
process_thread = threading.Thread(target=process_frames, daemon=True)

capture_thread.start()
process_thread.start()

# --------------------- Display ---------------------
while True:
    try:
        annotated = result_queue.get(timeout=1)
        scaled = cv2.resize(
            annotated,
            (display_width, display_height),
            interpolation=cv2.INTER_LANCZOS4
        )
        cv2.imshow("Fire Detection", scaled)
    except queue.Empty:
        continue

    if cv2.waitKey(1) & 0xFF == ord("q"):
        stop_event.set()
        break

capture_thread.join(timeout=2)
process_thread.join(timeout=2)
cap.release()
cv2.destroyAllWindows()