import streamlit as st
import cv2
import tempfile
import os

from ultralytics import YOLO

# Page settings
st.set_page_config(
    page_title="Object Detection and Tracking",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Object Detection and Tracking")
st.write("Upload a video to detect and track objects using YOLO.")

# Load YOLO model
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")


model = load_model()

# Upload video
uploaded_video = st.file_uploader(
    "Upload a video file",
    type=["mp4", "avi", "mov", "mkv"]
)

if uploaded_video is not None:

    # Save uploaded video temporarily
    video_bytes = uploaded_video.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp4"
    ) as temp_video:

        temp_video.write(video_bytes)
        input_video_path = temp_video.name

    # Open video
    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        st.error("Could not open the video.")
    else:
        st.success("Video loaded successfully.")

        frame_placeholder = st.empty()
        stop_button = st.button("Stop Processing")

        frame_count = 0

        while cap.isOpened():

            if stop_button:
                break

            success, frame = cap.read()

            if not success:
                break

            frame_count += 1

            # YOLO detection and tracking
            results = model.track(
                source=frame,
                persist=True,
                tracker="bytetrack.yaml",
                verbose=False
            )

            # Draw bounding boxes and tracking IDs
            annotated_frame = results[0].plot()

            # Convert BGR to RGB
            annotated_frame = cv2.cvtColor(
                annotated_frame,
                cv2.COLOR_BGR2RGB
            )

            # Display frame
            frame_placeholder.image(
                annotated_frame,
                channels="RGB",
                use_container_width=True
            )

        cap.release()

        st.success(
            f"Processing completed. Total frames: {frame_count}"
        )

    # Remove temporary file
    if os.path.exists(input_video_path):
        os.remove(input_video_path)