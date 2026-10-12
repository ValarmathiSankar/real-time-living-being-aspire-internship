import cv2

from src.analyzer import ActivityAnalyzer
from src.detector import LivingBeingDetector


class VideoProcessor:

    def __init__(self):
        self.detector = LivingBeingDetector()
        self.analyzer = ActivityAnalyzer()

    def process_frame(self, frame):
        """
        Process one video frame.

        Steps:
        1. Detect living beings
        2. Track objects
        3. Analyze movement
        4. Draw results
        """

        detections = self.detector.detect(frame)

        analyzed_detections = self.analyzer.analyze(
            detections
        )

        output_frame = self.detector.draw_detections(
            frame,
            analyzed_detections,
        )

        return output_frame, analyzed_detections

    def process_video(self, video_path):
        """
        Process a video file frame by frame.
        """

        capture = cv2.VideoCapture(video_path)

        if not capture.isOpened():
            raise ValueError(
                "Unable to open the video file."
            )

        while True:

            success, frame = capture.read()

            if not success:
                break

            output_frame, detections = self.process_frame(
                frame
            )

            yield output_frame, detections

        capture.release()