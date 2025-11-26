# FireFinder 🔥 by <a href="https://www.sushanka.com.np">SushankCode</a>

A real-time fire detection system using YOLOv8 and OpenCV that monitors camera feeds and alerts when fire is detected.

## Features

- **Real-time Detection**: Monitors live camera feed for fire detection
- **Confidence Filtering**: Configurable confidence threshold (default: 40%)
- **Frame-based Validation**: Requires multiple consecutive detections to reduce false positives
- **Visual Alerts**: Bounding boxes and warning messages on detected fire
- **Live Preview**: Real-time video display with detection overlays

## Requirements

- Python 3.8+
- OpenCV (`cv2`)
- Ultralytics YOLO
- Trained YOLO model weights

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd FireFinder
```

2. Install required dependencies:
```bash
pip install opencv-python ultralytics
```

3. Ensure your trained YOLO model is in the `models/` directory

## Project Structure

```
FireFinder/
├── Firefinder.py      # Main detection script
├── models/
│   ├── best.pt        # Best trained model weights
│   └── last.pt        # Last checkpoint weights
└── README.md          # This file
```

## Usage

Run the fire detection system:

```bash
python Firefinder.py
```

### Controls

- Press **'q'** to quit the application

### Configuration

You can adjust these parameters in `Firefinder.py`:

- `confidence_threshold`: Minimum confidence level for detection (default: 0.4)
- `fire_frame_threshold`: Number of consecutive frames needed to confirm fire (default: 3)
- Frame resolution: Currently set to 640x480

## How It Works

1. Captures video from the default camera (index 0)
2. Resizes each frame to 640x480 for consistent processing
3. Runs YOLOv8 inference on each frame
4. Filters detections by confidence threshold
5. Tracks consecutive fire detections to reduce false alarms
6. Displays bounding boxes and alerts when fire is confirmed

## Model

The system uses a custom-trained YOLOv8 model (`models/last.pt`) for fire detection. Ensure your model is properly trained on fire/flame datasets for optimal performance.

## Troubleshooting

- **"Cannot open camera"**: Check if your camera is connected and not being used by another application
- **Low detection accuracy**: Adjust the `confidence_threshold` or retrain the model with more data
- **False positives**: Increase the `fire_frame_threshold` value

