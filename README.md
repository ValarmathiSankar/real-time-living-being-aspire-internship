# Real-Time AI-Based Living Being Detection, Classification and Activity Analysis System

## 📌 Project Overview

The **Real-Time AI-Based Living Being Detection, Classification and Activity Analysis System** is an AI/ML-based application designed to detect, classify, track, and monitor living beings using images, videos, and live camera feeds.

The system uses computer vision and deep learning techniques to identify living beings such as people, dogs, cats, cows, and birds. It displays detection results through an interactive dashboard, including bounding boxes, confidence scores, object counts, tracking information, and basic movement analysis.

## 🎯 Objectives

- Detect living beings from images, videos, and camera feeds.
- Classify detected objects into supported categories.
- Track detected objects across video frames.
- Display detection counts and confidence scores.
- Analyze basic movement patterns, such as moving or stationary.
- Store detection events and timestamps in an SQLite database.
- Present results through an interactive Streamlit dashboard.

## ✨ Key Features

- **Living Being Detection:** Detects supported classes such as person, dog, cat, cow, and bird.
- **Object Tracking:** Tracks detected objects across video frames.
- **Real-Time Monitoring:** Processes live camera input, subject to system performance.
- **Movement Analysis:** Uses position changes to estimate basic movement.
- **Detection History:** Stores detection events with timestamps.
- **Interactive Dashboard:** Displays detection statistics, charts, and event information.
- **Confidence Threshold:** Allows detections to be filtered by confidence score.
- **Visual Results:** Shows bounding boxes and class labels on detected objects.

*Note: Features should be described as completed only after they have been implemented and tested in the project.*

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenCV | Image and video processing |
| YOLO (Ultralytics) | Object detection |
| ByteTrack | Object tracking |
| Streamlit | Interactive dashboard |
| SQLite | Detection event storage |
| Pandas | Data handling and analysis |
| NumPy | Numerical operations |

## 🏗️ System Architecture

The system follows this general workflow:

1. **Input:** Receive an image, video, or live camera feed.
2. **Preprocessing:** Prepare frames for detection.
3. **Detection:** Identify living beings using a YOLO model.
4. **Tracking:** Associate detections across frames using ByteTrack.
5. **Analysis:** Estimate basic movement using changes in object positions.
6. **Storage:** Save detection events and timestamps in SQLite.
7. **Visualization:** Display annotated frames, statistics, and history through Streamlit.

## 📁 Project Structure

```text
Real-Time-Living-Being-AI/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── detector.py
│   ├── analyzer.py
│   └── video_processor.py
│
└── outputs/
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.11
- pip package manager
- Webcam for live camera detection (optional)
- Internet connection for installing dependencies and downloading the pretrained model when needed

### 1. Clone the Repository

```bash
git clone https://github.com/ValarmathiSankar/Real-Time-Living-Being-AI.git
```

```bash
cd Real-Time-Living-Being-AI
```

Replace the repository URL if your GitHub repository uses a different name.

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
py -3.11 -m venv .venv
```

### 3. Activate the Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run app.py
```

Streamlit will provide a local URL in the terminal. Open that URL in your browser to access the dashboard.

## 🖥️ How to Use

1. Start the application.
2. Open the dashboard in your browser.
3. Select the available input mode.
4. Upload an image or video, or select the webcam option if supported.
5. Adjust the confidence threshold if the interface provides the option.
6. View detected objects, labels, confidence scores, and tracking information.
7. Review available statistics and detection history.

## 📊 Expected Output

Depending on the implemented features and selected input, the application may display:

- Annotated images or video frames.
- Detected object classes and confidence scores.
- Object counts and tracking IDs.
- Basic movement status.
- Detection timestamps and event history.
- Dashboard charts and summary statistics.

Actual detection accuracy and processing speed depend on the model, input quality, and hardware. Record measured results after testing the application.

## ⚠️ Limitations

- Detection is limited to the classes supported by the selected pretrained model and the configured class filter.
- Movement analysis based on position changes is a basic estimate, not a complete activity-recognition system.
- Detection results may vary with lighting, camera angle, distance, and occlusion.
- Real-time performance depends on available computing resources.
- The system should not be treated as a guaranteed safety or security solution.

## 🚀 Future Enhancements

- Add advanced activity recognition.
- Improve tracking across crowded scenes.
- Introduce configurable monitoring zones.
- Add event notifications and alert history.
- Support additional living-being categories.
- Improve dashboard analytics and reporting.
- Evaluate model accuracy and processing performance on a test dataset.

## 👩‍💻 Developer

**Valarmathi S**  
B.Tech – Artificial Intelligence and Data Science  
Anand Institute of Higher Technology

