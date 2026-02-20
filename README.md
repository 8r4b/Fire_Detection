# Fire Detection System

A real-time fire detection system using YOLOv8 object detection model. This project supports multiple camera sources including webcams, ESP32-CAM devices, and Raspberry Pi cameras.

## Features

- Real-time fire detection using YOLOv8
- Support for multiple camera inputs:
  - Webcam
  - ESP32-CAM
- Alert notifications via API
- Custom dataset support

## Project Structure

```
Fire_Detection/
├── esp_cam.py              # ESP32-CAM integration
├── esp_cam_alert.py        # ESP32-CAM with alerts
├── rasp_cam.py             # Raspberry Pi camera integration
├── webcam.py               # Webcam detection
├── train.py                # Model training script
├── split.py                # Dataset split utility
├── vapi_call.py            # API calls for notifications
├── fire_dataset.yaml       # Dataset configuration
├── dataset/                # Training dataset
├── fire_detected/          # Detected fire results
└── requirements.txt        # Python dependencies
```

## Installation

### Prerequisites

- Python 3.8 or higher
- CUDA-capable GPU (recommended for faster inference)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Fire_Detection
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run Detection on Webcam
```bash
python webcam.py
```

### Run Detection on ESP32-CAM
```bash
python esp_cam.py
```

### Train Model on Custom Dataset
```bash
python train.py
```

### Split Dataset
```bash
python split.py
```

## Dataset

The project uses a custom fire detection dataset. Configure the dataset path in `fire_dataset.yaml`.

## Model

This project uses YOLOv8 (Ultralytics) for object detection. Pre-trained weights are automatically downloaded during first run.

## Dependencies

See [requirements.txt](requirements.txt) for complete list:
- ultralytics (YOLOv8)
- torch
- torchvision
- opencv-python
- numpy
- matplotlib
- pandas
- PyYAML

## Configuration

Edit `fire_dataset.yaml` to configure:
- Dataset paths
- Class names
- Model parameters

## License

[Add your license here]

## Contributing

Feel free to submit issues and enhancement requests!

## Author

[Your Name/Team]

## Acknowledgments

- Ultralytics YOLOv8
- PyTorch and torchvision communities
