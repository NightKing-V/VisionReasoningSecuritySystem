import streamlit as st
from yolo_detector import detect_objects
from llm_agent import analyze_scene
from utils import load_image

st.set_page_config(page_title="🛡️ Security Scene Analyzer", layout="centered")
st.title("🛡️ Visual Security Assistant")

uploaded_file = st.file_uploader("📷 Upload an image for security analysis", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = load_image(uploaded_file.read())
    st.image(image, caption="Uploaded Image", use_container_width=True)

    with st.spinner("🔍 Detecting objects..."):
        labels, annotated_image = detect_objects(image)

    st.success("✅ Objects Detected")
    st.image(annotated_image, caption="Detected Objects", use_container_width=True)
    st.write("### 🏷️ Detected Labels")
    st.write(labels)

    with st.spinner("🤖 Analyzing scene..."):
        reasoning = analyze_scene(labels)

    st.write("### 🧠 Scene Analysis")
    st.markdown(reasoning)
