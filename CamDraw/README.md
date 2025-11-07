# CamDraw — Hand Paint with MediaPipe & OpenCV-<a href="https://sushanka.com.np">SushankCode</a>

A small, interactive hand-painting demo using MediaPipe Hands and OpenCV. Use your webcam and a pinch gesture (thumb + index fingertip) to toggle drawing, or tap the colored buttons at the top of the window to change color or select the eraser.

This repository contains a single script:

- `camdraw.py` — the main program. It captures webcam frames, detects a single hand with MediaPipe, shows a top color selection bar, and lets you draw on a virtual canvas.

## Features

- Real-time hand tracking using MediaPipe Hands
- Pinch-to-toggle drawing (thumb + index fingertip distance)
- On-screen color palette (Red, Green, Blue, Yellow, Eraser)
- Eraser mode (large brush)
- Visual feedback for drawing mode and live hand landmarks

## Quick start (Windows PowerShell)

1. Ensure you have Python 3.8+ installed.
2. Install dependencies listed in `Requirment.txt` (note the file name in the project). From the project folder run:

```powershell
python -m pip install -r .\Requirment.txt
```

3. Run the application:

```powershell
python .\camdraw.py
```

4. A window named `Hand Paint` will open. Point your webcam at your hand and interact.

If your camera is not device 0, open `camdraw.py` and change `cv2.VideoCapture(0)` to the correct index.

## How to use

- Color selection: move the index fingertip into the top area and hover/tap one of the colored rectangles to select a color or the eraser.
- Toggle drawing: pinch (bring thumb and index fingertip together). The script toggles drawing mode on the pinch rising edge so a single pinch toggles ON, another pinch toggles OFF. This prevents accidentally switching mode while moving.
- While drawing: the index fingertip draws continuous strokes; the eraser uses a larger thickness.
- Quit: press `q` in the window to exit.

## Configuration (in `camdraw.py`)

Key parameters you may want to tune:

- `pinch_threshold` (default 40) — maximum pixel distance between thumb and index to consider a pinch. Lower for less sensitivity, higher for more sensitivity. Pixel-based, so depends on camera resolution and distance.
- `draw_thickness` (default 6) — brush thickness when drawing with colors.
- `eraser_thickness` (default 50) — thickness used for eraser mode.
- `max_num_hands` — currently set to 1. Increase if you want multi-hand support (needs logic changes).
- Frame size: the script sets the camera resolution with `cv2.CAP_PROP_FRAME_WIDTH` and `cv2.CAP_PROP_FRAME_HEIGHT` — change these to trade off accuracy vs. performance.

## Troubleshooting & tips

- If hand landmarks are jittery, try increasing `min_tracking_confidence` or reducing the camera resolution.
- If the pinch doesn't register reliably:
  - Move your hand closer/farther to change pixel distance.
  - Adjust `pinch_threshold` in `camdraw.py`.
- If colors appear wrong or the UI rectangles are off-screen at smaller windows, resize the OpenCV window or adjust `button_width`/`button_height` values.
- If `Requirment.txt` isn't present or dependencies fail to install, ensure you have `mediapipe`, `opencv-python` and `numpy` installed:

```powershell
python -m pip install mediapipe opencv-python numpy
```

## Contract / expected behavior

- Input: webcam frames (camera). Interaction via hand gestures (index/thumb) and on-screen touches with the index fingertip.
- Output: OpenCV window showing live camera feed with landmarks and drawn canvas composited on top.
- Error modes: no camera -> script will fail to open capture; no hand detected -> drawing pauses until hand returns; wrong camera index -> no frames.

## Edge cases

- Low light may reduce detection accuracy.
- Very fast hand motion may cause dropped frames or missed landmark detection.
- Multiple hands in view will still be processed but the script is tuned for a single hand.

## Next steps / improvements

- Add a UI to change parameters at runtime (sliders for threshold and thickness).
- Implement continuous drawing while pinched (instead of toggle) as an option.
- Save/load drawings to disk.
- Add multi-hand support and per-hand canvas layers.



If you want, I can:

- add a `README` badge and an example GIF showing drawing
- add a `requirements.txt` with pinned versions
- add a short troubleshooting script to test camera availability


