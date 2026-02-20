import cv2
from ultralytics import YOLO
import threading
import queue
import socket
import json
import time

model = YOLO("C:/Users/msi-pc/OneDrive/سطح المكتب/best.pt")

# Alert relay configuration
RELAY_SERVER_HOST = "127.0.0.1"  # Change to relay computer IP if on different machine
RELAY_SERVER_PORT = 9999
ENABLE_RELAY_ALERTS = True  # Set to False to disable alerts

stream_url = "http://192.168.1.1:81/stream"
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Cannot open ESP32 stream")
    exit()

cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Get original frame dimensions
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Scale factor (1.5 = 150% of original size, adjust as needed)
scale_factor = 2.1
display_width = int(frame_width * scale_factor)
display_height = int(frame_height * scale_factor)

# Queue to store frames and results
frame_queue = queue.Queue(maxsize=2)
result_queue = queue.Queue(maxsize=1)
stop_event = threading.Event()

def capture_frames():
    """Continuously capture frames from stream at native FPS"""
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            continue
        try:
            frame_queue.put(frame, block=False)
        except queue.Full:
            pass  # Skip if queue is full, prioritize fresh frames

def send_fire_alert(confidence, image_path):
    """Send fire alert to relay server"""
    if not ENABLE_RELAY_ALERTS:
        return
    
    try:
        alert_data = json.dumps({
            "confidence": float(confidence),
            "image_path": image_path,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(alert_data.encode(), (RELAY_SERVER_HOST, RELAY_SERVER_PORT))
        sock.close()
        
        print(f"[ALERT] Fire alert sent to relay: {confidence:.2%}")
    except Exception as e:
        print(f"[ERROR] Failed to send alert: {e}")

def capture_frames():
    """Continuously capture frames from stream at native FPS"""
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            continue
        try:
            frame_queue.put(frame, block=False)
        except queue.Full:
            pass  # Skip if queue is full, prioritize fresh frames

def process_frames():
    """Process frames with YOLO asynchronously"""
    while not stop_event.is_set():
        try:
            frame = frame_queue.get(timeout=1)
            results = model(frame, imgsz=320, verbose=False)
            annotated = results[0].plot()
            try:
                result_queue.put(annotated, block=False)
            except queue.Full:
                pass
        except queue.Empty:
            continue

# Start capture and processing threads
capture_thread = threading.Thread(target=capture_frames, daemon=True)
process_thread = threading.Thread(target=process_frames, daemon=True)

capture_thread.start()
process_thread.start()

while True:
    try:
        annotated = result_queue.get(timeout=1)
        # Scale up the frame using INTER_LANCZOS4 for high-quality upsampling
        scaled = cv2.resize(annotated, (display_width, display_height), interpolation=cv2.INTER_LANCZOS4)
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
