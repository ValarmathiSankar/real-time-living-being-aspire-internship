import threading
import time


class DetectionState:

    def __init__(self):

        self.lock = threading.Lock()

        # Current detections
        self.detections = []

        # Total processed frames
        self.frame_count = 0

        # FPS
        self.fps = 0.0

        # Detection statistics
        self.total_detection_count = 0

        self.object_totals = {}

        # Current alerts
        self.alerts = []

        # Current zone information
        self.zone_counts = {}

        # Last update
        self.last_update = time.time()


SHARED_STATE = DetectionState()