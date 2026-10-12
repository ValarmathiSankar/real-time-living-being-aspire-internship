import sqlite3
from datetime import datetime

from src.config import DATABASE_PATH


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            DATABASE_PATH,
            check_same_thread=False,
        )

        self.create_tables()


    # ========================================================
    # CREATE TABLES
    # ========================================================

    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS detection_events (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                timestamp TEXT NOT NULL,

                object_type TEXT NOT NULL,

                tracking_id INTEGER,

                confidence REAL,

                activity TEXT,

                movement_distance REAL,

                event TEXT,

                zone TEXT

            )
            """
        )

        # --------------------------------------------------------
        # DATABASE MIGRATION
        # --------------------------------------------------------
        # Check which columns already exist

        cursor.execute(
            "PRAGMA table_info(detection_events)"
        )

        existing_columns = {
            row[1]
            for row in cursor.fetchall()
        }

        # Add zone column if this is an older database
        if "zone" not in existing_columns:

            cursor.execute(
                """
                ALTER TABLE detection_events
                ADD COLUMN zone TEXT
                """
            )


    

        self.connection.commit()


    # ========================================================
    # ADD EVENT
    # ========================================================

    def add_event(
        self,
        object_type,
        tracking_id,
        confidence,
        activity,
        movement_distance,
        event,
        zone=None,
    ):

        cursor = self.connection.cursor()

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute(
            """
            INSERT INTO detection_events
            (
                timestamp,
                object_type,
                tracking_id,
                confidence,
                activity,
                movement_distance,
                event,
                zone
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                object_type,
                tracking_id,
                confidence,
                activity,
                movement_distance,
                event,
                zone,
            ),
        )

        self.connection.commit()


    # ========================================================
    # RECENT EVENTS
    # ========================================================

    def get_recent_events(self, limit=100):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                timestamp,
                object_type,
                tracking_id,
                confidence,
                activity,
                movement_distance,
                event,
                zone

            FROM detection_events

            ORDER BY id DESC

            LIMIT ?
            """,
            (limit,),
        )

        return cursor.fetchall()


    # ========================================================
    # TOTAL DETECTIONS
    # ========================================================

    def get_total_detections(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM detection_events
            """
        )

        result = cursor.fetchone()

        return result[0]


    # ========================================================
    # OBJECT COUNTS
    # ========================================================

    def get_object_counts(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                object_type,
                COUNT(*)

            FROM detection_events

            GROUP BY object_type

            ORDER BY COUNT(*) DESC
            """
        )

        return cursor.fetchall()


    # ========================================================
    # CLOSE
    # ========================================================

    def close(self):

        self.connection.close()