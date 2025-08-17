import streamlit as st
import cv2
import time
from cam_detector import list_available_cameras
from telegrambot import send_telegram_status
from model import ThreatDetectionModel

st.set_page_config(page_title="Surveillance System", layout="centered")

# Initialize model
detector = ThreatDetectionModel(target_classes=['Armed-Person', 'Rifle', 'Person', 'knife'])
st.title("🔫 Real-time Surveilance System")
send_telegram_status("Threat Detection App Started")

# Initialize session state
if "running" not in st.session_state:
    st.session_state.running = False
if "cap" not in st.session_state:
    st.session_state.cap = None

# Camera selection
st.markdown("### 🎥 Select or enter a camera source:")
cam_source_type = st.radio("Choose source type", ["Webcam", "Mobile IP Camera"])

if cam_source_type == "Webcam":
    available_cams = list_available_cameras()
    selected_cam = st.selectbox("Camera Index", available_cams)
else:
    selected_cam = st.text_input("Enter IP camera URL (e.g. http://192.168.xxx.xxx:xxxx/video)")

# Start/Stop buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start Now"):
        if not st.session_state.running:
            st.session_state.running = True
            st.session_state.cap = cv2.VideoCapture(
                selected_cam if isinstance(selected_cam, str) and selected_cam.startswith("http") 
                else int(selected_cam)
            )
with col2:
    if st.button("🛑 Stop"):
        st.session_state.running = False
        if st.session_state.cap:
            st.session_state.cap.release()
            st.session_state.cap = None
        cv2.destroyAllWindows()

frame_placeholder = st.empty()
detected_classes = st.empty()

# Live detection loop
while st.session_state.running and st.session_state.cap:
    ret, frame = st.session_state.cap.read()
    if not ret:
        st.error("Failed to grab frame.")
        break

    processed_frame, detections = detector.infer(frame)

    # Show frame in Streamlit
    frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
    frame_placeholder.image(frame_rgb, channels="RGB")

    if detections:
        detected_classes.markdown(f"⚠️ Detected: **{', '.join(detections)}**")

    time.sleep(0.03)  # ~30 FPS
