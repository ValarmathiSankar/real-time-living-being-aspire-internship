import cv2

from ultralytics import YOLO

from src.config import (
    MODEL_NAME,
    CONFIDENCE_THRESHOLD,
    IOU_THRESHOLD,
    SUPPORTED_CLASSES,
)


class LivingBeingDetector:
    def __init__(self):
        self.model = YOLO(MODEL_NAME)

    def detect(self, frame):
        """
        Detect living beings in a single image frame.
        """

        results = self.model.track(
            frame,
            persist=True,
            conf=CONFIDENCE_THRESHOLD,
            iou=IOU_THRESHOLD,
            verbose=False,
        )

        detections = []

        if not results:
            return detections

        result = results[0]

        if result.boxes is None:
            return detections

        boxes = result.boxes

        for i in range(len(boxes)):
            class_id = int(boxes.cls[i].item())
            confidence = float(boxes.conf[i].item())

            class_name = self.model.names[class_id]

            if class_name not in SUPPORTED_CLASSES:
                continue

            coordinates = boxes.xyxy[i].cpu().numpy().tolist()

            tracking_id = None

            if boxes.id is not None:
                tracking_id = int(boxes.id[i].item())

            detections.append(
                {
                    "class_name": class_name,
                    "confidence": confidence,
                    "bbox": coordinates,
                    "track_id": tracking_id,
                }
            )

        return detections
    def draw_detections(self, frame, detections):
        """
        Draw bounding boxes and labels on the frame.
        """

        for detection in detections:
            x1, y1, x2, y2 = map(int, detection["bbox"])

            class_name = detection["class_name"]
            confidence = detection["confidence"]
            track_id = detection["track_id"]

            if track_id is not None:
                label = f"{class_name} #{track_id} {confidence:.2f}"
            else:
                label = f"{class_name} {confidence:.2f}"

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2,
            )

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

        return frame