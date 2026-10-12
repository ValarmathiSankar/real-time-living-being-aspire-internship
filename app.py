import time
from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st

from streamlit_webrtc import (
    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)

from src.detector import LivingBeingDetector
from src.analyzer import ActivityAnalyzer
from src.shared_state import SHARED_STATE
from src.database import Database


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Real-Time Living Being AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROFESSIONAL DARK UI
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 12px;
    }

    /* Headers */
    h1, h2, h3 {
        color: #ffffff;
    }

    /* Info boxes */
    .status-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
    }

    /* Alert */
    .alert-card {
        background-color: #2b1717;
        border-left: 4px solid #ff4b4b;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
    }

    /* Success */
    .success-card {
        background-color: #14261a;
        border-left: 4px solid #21c55d;
        border-radius: 8px;
        padding: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATABASE
# ============================================================

db = Database()


# ============================================================
# LIVE VIDEO PROCESSOR
# ============================================================

class LiveVideoProcessor(VideoProcessorBase):

    def __init__(self):

        self.detector = LivingBeingDetector()

        self.analyzer = ActivityAnalyzer()

        self.last_fps_time = time.time()

        self.fps_frame_count = 0


    def recv(self, frame):

        image = frame.to_ndarray(
            format="bgr24"
        )

        # ----------------------------------------------------
        # YOLO DETECTION
        # ----------------------------------------------------

        detections = self.detector.detect(
            image
        )

        # ----------------------------------------------------
        # ACTIVITY ANALYSIS
        # ----------------------------------------------------

        detections = self.analyzer.analyze(
            detections
        )

        # ----------------------------------------------------
        # FPS CALCULATION
        # ----------------------------------------------------

        self.fps_frame_count += 1

        current_time = time.time()

        elapsed = (
            current_time
            -
            self.last_fps_time
        )

        if elapsed >= 1.0:

            fps = (
                self.fps_frame_count
                /
                elapsed
            )

            with SHARED_STATE.lock:

                SHARED_STATE.fps = round(
                    fps,
                    1
                )

            self.fps_frame_count = 0

            self.last_fps_time = current_time

        # ----------------------------------------------------
        # UPDATE SHARED STATE
        # ----------------------------------------------------

        with SHARED_STATE.lock:

            SHARED_STATE.detections = (
                detections.copy()
            )

            SHARED_STATE.frame_count += 1

            SHARED_STATE.last_update = (
                current_time
            )

        # ----------------------------------------------------
        # UPDATE STATISTICS
        # ----------------------------------------------------

        for detection in detections:

            object_name = detection[
                "class_name"
            ]

            with SHARED_STATE.lock:

                if object_name not in (
                    SHARED_STATE.object_totals
                ):

                    SHARED_STATE.object_totals[
                        object_name
                    ] = 0

                SHARED_STATE.object_totals[
                    object_name
                ] += 1

                SHARED_STATE.total_detection_count += 1

        # ----------------------------------------------------
        # RAPID MOVEMENT ALERT
        # ----------------------------------------------------

        for detection in detections:

            if (
                detection["event"]
                == "Rapid Movement Detected"
            ):

                alert = {
                    "time": time.strftime(
                        "%H:%M:%S"
                    ),

                    "object": detection[
                        "class_name"
                    ],

                    "track_id": detection[
                        "track_id"
                    ],

                    "activity": detection[
                        "activity"
                    ],
                }

                with SHARED_STATE.lock:

                    SHARED_STATE.alerts.append(
                        alert
                    )

                    # Keep latest 20 alerts
                    SHARED_STATE.alerts = (
                        SHARED_STATE.alerts[
                            -20:
                        ]
                    )

                # Save to database
                db.add_event(
                    object_type=detection[
                        "class_name"
                    ],

                    tracking_id=detection[
                        "track_id"
                    ],

                    confidence=detection[
                        "confidence"
                    ],

                    activity=detection[
                        "activity"
                    ],

                    movement_distance=detection[
                        "movement_distance"
                    ],

                    event=detection[
                        "event"
                    ],
                )

        # ----------------------------------------------------
        # DRAW
        # ----------------------------------------------------

        output = (
            self.detector.draw_detections(
                image,
                detections
            )
        )

        return frame.from_ndarray(
            output,
            format="bgr24"
        )


# ============================================================
# HEADER
# ============================================================

st.title(
    "🤖 Real-Time Living Being AI"
)

st.caption(
    "AI-powered detection • tracking • activity analysis • real-time analytics"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Controls")

    st.subheader(
        "Detection Settings"
    )

    confidence = st.slider(
        "Confidence Threshold",
        min_value=0.10,
        max_value=0.95,
        value=0.40,
        step=0.05,
    )

    st.caption(
        f"Current threshold: {confidence:.2f}"
    )

    st.divider()

    rapid_alerts = st.toggle(
        "🚨 Rapid movement alerts",
        value=True,
    )

    save_history = st.toggle(
        "💾 Save detection history",
        value=True,
    )

    st.divider()

    st.subheader(
        "📊 System"
    )

    st.write(
        "YOLO: `YOLO11n`"
    )

    st.write(
        "Tracking: `Enabled`"
    )

    st.write(
        "Database: `SQLite`"
    )

    st.write(
        "Dashboard: `Live`"
    )


# ============================================================
# CAMERA
# ============================================================

st.header(
    "📹 Live Camera"
)

ctx = webrtc_streamer(

    key="living-being-camera",

    mode=WebRtcMode.SENDRECV,

    video_processor_factory=LiveVideoProcessor,

    media_stream_constraints={
        "video": True,
        "audio": False,
    },

    async_processing=True,
)


if ctx.state.playing:

    st.success(
        "🟢 Camera running — AI detection active"
    )

else:

    st.info(
        "Click START to activate the camera."
    )


# ============================================================
# LIVE DASHBOARD
# ============================================================

@st.fragment(run_every=0.5)
def dashboard():

    # --------------------------------------------------------
    # READ SHARED STATE
    # --------------------------------------------------------

    with SHARED_STATE.lock:

        detections = (
            SHARED_STATE.detections.copy()
        )

        frame_count = (
            SHARED_STATE.frame_count
        )

        fps = (
            SHARED_STATE.fps
        )

        total_detection_count = (
            SHARED_STATE.total_detection_count
        )

        object_totals = (
            SHARED_STATE.object_totals.copy()
        )

        alerts = (
            SHARED_STATE.alerts.copy()
        )

    # ========================================================
    # TOP METRICS
    # ========================================================

    st.divider()

    st.header(
        "📊 Live Dashboard"
    )

    counts = Counter(
        detection["class_name"]
        for detection in detections
    )

    total_objects = len(
        detections
    )

    moving = sum(
        1
        for detection in detections
        if detection["activity"]
        != "Stationary"
    )

    stationary = sum(
        1
        for detection in detections
        if detection["activity"]
        == "Stationary"
    )

    person_count = counts.get(
        "person",
        0
    )

    animal_count = sum(
        counts.get(
            animal,
            0
        )
        for animal in [
            "dog",
            "cat",
            "cow",
            "bird",
        ]
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4, col5, col6 = (
        st.columns(6)
    )

    with col1:

        st.metric(
            "👤 Persons",
            person_count
        )

    with col2:

        st.metric(
            "🐾 Animals",
            animal_count
        )

    with col3:

        st.metric(
            "🎯 Objects",
            total_objects
        )

    with col4:

        st.metric(
            "🏃 Moving",
            moving
        )

    with col5:

        st.metric(
            "🧍 Stationary",
            stationary
        )

    with col6:

        st.metric(
            "⚡ FPS",
            fps
        )

    # ========================================================
    # SECONDARY STATS
    # ========================================================

    st.divider()

    col1, col2, col3 = (
        st.columns(3)
    )

    with col1:

        st.metric(
            "📈 Total Detections",
            total_detection_count
        )

    with col2:

        if object_totals:

            most_detected = max(
                object_totals,
                key=object_totals.get
            )

            st.metric(
                "🏆 Most Detected",
                most_detected
            )

        else:

            st.metric(
                "🏆 Most Detected",
                "-"
            )

    with col3:

        st.metric(
            "🧠 Frames Processed",
            frame_count
        )

    # ========================================================
    # CHARTS
    # ========================================================

    st.divider()

    st.header(
        "📊 Detection Analytics"
    )

    chart_col1, chart_col2 = (
        st.columns(2)
    )

    # --------------------------------------------------------
    # OBJECT DISTRIBUTION
    # --------------------------------------------------------

    with chart_col1:

        st.subheader(
            "Object Distribution"
        )

        if object_totals:

            df_objects = pd.DataFrame(
                {
                    "Object": list(
                        object_totals.keys()
                    ),

                    "Detections": list(
                        object_totals.values()
                    ),
                }
            )

            fig = px.bar(
                df_objects,
                x="Object",
                y="Detections",
                title="Detection Count by Object",
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0e1117",
                plot_bgcolor="#0e1117",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:

            st.info(
                "Waiting for detection data..."
            )

    # --------------------------------------------------------
    # CURRENT ACTIVITY
    # --------------------------------------------------------

    with chart_col2:

        st.subheader(
            "Current Activity"
        )

        activity_counts = Counter(
            detection["activity"]
            for detection in detections
        )

        if activity_counts:

            df_activity = pd.DataFrame(
                {
                    "Activity": list(
                        activity_counts.keys()
                    ),

                    "Count": list(
                        activity_counts.values()
                    ),
                }
            )

            fig = px.pie(
                df_activity,
                names="Activity",
                values="Count",
                title="Current Activity",
                hole=0.45,
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0e1117",
                plot_bgcolor="#0e1117",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:

            st.info(
                "No activity data yet."
            )

    # ========================================================
    # RAPID MOVEMENT ALERTS
    # ========================================================

    st.divider()

    st.header(
        "🚨 Alerts"
    )

    if rapid_alerts and alerts:

        for alert in reversed(
            alerts[-10:]
        ):

            st.markdown(
                f"""
                <div class="alert-card">

                ⚠️ <b>{alert["time"]}</b>

                &nbsp;&nbsp;

                {alert["object"]}

                #{alert["track_id"]}

                — {alert["activity"]}

                </div>
                """,
                unsafe_allow_html=True,
            )

    else:

        st.success(
            "No rapid movement alerts."
        )

    # ========================================================
    # INDIVIDUAL TRACKED OBJECTS
    # ========================================================

    st.divider()

    st.header(
        "🐾 Individual Tracked Objects"
    )

    if detections:

        object_rows = []

        for detection in detections:

            object_rows.append(
                {
                    "Object":
                        detection[
                            "class_name"
                        ],

                    "Track ID":
                        detection[
                            "track_id"
                        ],

                    "Confidence":
                        round(
                            detection[
                                "confidence"
                            ],
                            2,
                        ),

                    "Activity":
                        detection[
                            "activity"
                        ],

                    "Movement":
                        detection[
                            "movement_distance"
                        ],

                    "Speed":
                        detection.get(
                            "speed",
                            0,
                        ),
                }
            )

        df = pd.DataFrame(
            object_rows
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No supported living beings detected."
        )

    # ========================================================
    # DETECTION HISTORY
    # ========================================================

    st.divider()

    st.header(
        "🕒 Detection History"
    )

    if save_history:

        history = (
            db.get_recent_events(
                limit=50
            )
        )

        if history:

            history_df = pd.DataFrame(
                history,
                columns=[
                    "Timestamp",
                    "Object",
                    "Track ID",
                    "Confidence",
                    "Activity",
                    "Movement",
                    "Event",
                    "Zone",
                ],
            )

            st.dataframe(
                history_df,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "No saved detection events yet."
            )

    else:

        st.info(
            "Detection history saving is disabled."
        )


# ============================================================
# RUN DASHBOARD
# ============================================================

dashboard()