from ultralytics import YOLO

# Load a pre-defined YOLOv8 model (e.g., nano, small, medium)
model = YOLO("yolov8n.pt")  # yolov8n.pt is lightweight, good for testing

# Train the model
model.train(
    data="fire_dataset.yaml",   # path to your dataset config
    epochs=50,          # adjust number of epochs
    imgsz=640,          # image size
    batch=16,           # batch size
    name="fire_detector" # name of your experiment
)
