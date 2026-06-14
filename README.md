# Gesture Control Presenter 🎮🖐️

Control presentation slides using hand gestures and a webcam. Built using Computer Vision and AI with MediaPipe and OpenCV.

## Features

- Next Slide using hand gestures
- Previous Slide using hand gestures
- Start Presentation
- Exit Presentation
- Real-time Hand Tracking
- Laser Pointer Mode
- FPS Monitoring
- Gesture Stabilization to prevent accidental triggers

## Technologies Used

- Python
- OpenCV
- MediaPipe
- PyAutoGUI

## Project Structure

```
gesture_control_main/
│
├── models/
│   └── hand_landmarker.task
├── main.py
├── setup_models.py
├── requirements.txt
└── README.md
```

## Installation

### Clone Repository

```bash
git clone https://github.com/anushka1719/gesture_control_main.git
cd gesture_control_main
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Download Model

```bash
python setup_models.py
```

### Run Application

```bash
python main.py
```

## Gesture Controls

| Gesture | Action |
|----------|----------|
| Open Palm | Next Slide |
| Three Fingers | Previous Slide |
| Two Fingers | Start Presentation |
| Fist | Exit Presentation |
| One Finger | Laser Pointer Mode |

## Screenshots

### Main Interface

The application detecting hand landmarks in real time using MediaPipe and OpenCV.

![Main Interface](images/main_interface.png)

### Laser Pointer Mode

Laser pointer functionality controlled using hand gestures for presentation assistance.

![Laser Pointer](images/laser_pointer.png)

## Learning Outcomes

- Computer Vision
- Hand Landmark Detection
- Human Computer Interaction
- Real-Time Video Processing
- Python Automation

## Author

Anushka
