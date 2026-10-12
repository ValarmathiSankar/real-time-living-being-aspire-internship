import math
import time

from src.config import (
    MOVEMENT_THRESHOLD,
    RAPID_MOVEMENT_THRESHOLD,
)


class ActivityAnalyzer:

    def __init__(self):

        self.previous_positions = {}

        self.previous_times = {}


    # ========================================================
    # CENTER OF BOUNDING BOX
    # ========================================================

    def _get_center(self, bbox):

        x1, y1, x2, y2 = bbox

        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        return center_x, center_y


    # ========================================================
    # ACTIVITY ANALYSIS
    # ========================================================

    def analyze(self, detections):

        analyzed = []

        current_time = time.time()

        for detection in detections:

            track_id = detection.get(
                "track_id"
            )

            bbox = detection["bbox"]

            center_x, center_y = (
                self._get_center(bbox)
            )

            movement_distance = 0.0

            speed = 0.0

            # ------------------------------------------------
            # TRACKED OBJECT
            # ------------------------------------------------

            if (
                track_id is not None
                and track_id in self.previous_positions
            ):

                previous_x, previous_y = (
                    self.previous_positions[
                        track_id
                    ]
                )

                movement_distance = math.sqrt(
                    (center_x - previous_x) ** 2
                    +
                    (center_y - previous_y) ** 2
                )

                previous_time = (
                    self.previous_times.get(
                        track_id,
                        current_time
                    )
                )

                time_difference = (
                    current_time
                    -
                    previous_time
                )

                if time_difference > 0:

                    speed = (
                        movement_distance
                        /
                        time_difference
                    )

            # ------------------------------------------------
            # SAVE CURRENT POSITION
            # ------------------------------------------------

            if track_id is not None:

                self.previous_positions[
                    track_id
                ] = (
                    center_x,
                    center_y,
                )

                self.previous_times[
                    track_id
                ] = current_time

            # ------------------------------------------------
            # CLASSIFY ACTIVITY
            # ------------------------------------------------

            if (
                movement_distance
                >= RAPID_MOVEMENT_THRESHOLD
            ):

                activity = "Rapid Movement"

                event = (
                    "Rapid Movement Detected"
                )

            elif (
                movement_distance
                >= MOVEMENT_THRESHOLD
            ):

                activity = "Moving"

                event = None

            else:

                activity = "Stationary"

                event = None

            # ------------------------------------------------
            # RESULT
            # ------------------------------------------------

            result = detection.copy()

            result[
                "movement_distance"
            ] = round(
                movement_distance,
                2,
            )

            result[
                "speed"
            ] = round(
                speed,
                2,
            )

            result[
                "activity"
            ] = activity

            result[
                "event"
            ] = event

            analyzed.append(result)

        return analyzed