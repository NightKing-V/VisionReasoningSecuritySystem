import streamlit as st
import cv2
from ultralytics import YOLO
from cam_detector import list_available_cameras
import time
from telegrambot import send_telegram_alert, send_telegram_status

st.set_page_config(page_title="Weapon Detection", layout="centered")

# Load the trained model
model = YOLO("app/best.pt")
target_classes = ['pistol', 'knife']
last_alert_time = 0

st.title("🔫 Real-time Weapon Detection")
send_telegram_status("Weapon Detection App Started")

# Camera selection
st.markdown("### 🎥 Select or enter a camera source:")
cam_source_type = st.radio("Choose source type", ["Webcam", "Mobile IP Camera"])

if cam_source_type == "Webcam":
    available_cams = list_available_cameras()
    selected_cam = st.selectbox("Camera Index", available_cams)
else:
    selected_cam = st.text_input("Enter IP camera URL (e.g. http://192.168.xxx.xxx:xxxx/video)")

start_btn = st.button("▶️ Start Now")

# Display frames and detections
frame_placeholder = st.empty()
detected_classes = st.empty()

if start_btn:
    if isinstance(selected_cam, str) and selected_cam.startswith("http"):
        cap = cv2.VideoCapture(selected_cam)
    else:
        cap = cv2.VideoCapture(int(selected_cam))

    st.info("🔍 Detecting... press 'q' to stop in the webcam window.")

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to grab frame.")
            break

        # Inference
        results = model(frame, stream=True)
        current_detections = set()

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                name = model.names[cls_id]

                # Draw bounding box
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{name} {conf:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                if name in target_classes:
                    current_detections.add(name)

        # Show in Streamlit
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame_rgb, channels="RGB")

        if current_detections:
            detected_classes.markdown(f"⚠️ Detected: **{', '.join(current_detections)}**")
        
            # Telegram alert with cooldown
            if time.time() - last_alert_time > 10:
                send_telegram_alert(current_detections)
                last_alert_time = time.time()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    st.success("🛑 Detection stopped.")
