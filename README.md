# VisionReasoningSecuritySystem

| **Category**        | **Tool / Tech**                                    | **Purpose / Description**                                      |
| ------------------- | -------------------------------------------------- | -------------------------------------------------------------- |
| 🧠 ML Model         | YOLOv8 (Ultralytics)                               | Object detection model fine-tuned for weapon detection         |
|                     | PyTorch `.pt`                                      | Model format used during inference                             |
| 🏋️ Training        | Transfer Learning                                  | Trained with custom dataset (Roboflow)                         |
| 📁 Dataset Format   | YOLO (labels `.txt`, `data.yaml`)                  | Used for training, validation, and inference                   |
| 🧪 Inference Engine | `ultralytics` Python package                       | Handles model loading and inference pipeline                   |
| 🎥 Video Input      | OpenCV (`cv2.VideoCapture`)                        | Captures webcam or mobile stream                               |
|                     | Custom cam selector (`list_available_cameras()`)   | Lists available webcams and IP streams                         |
| 📱 IP Streaming     | IP Webcam                                          | Sends mobile camera feed over local network                    |
| 🌐 UI Framework     | Streamlit                                          | Real-time interactive web app with live video + controls       |
| 📦 Deployment       | Docker                                             | Containerized deployment of the app                            |
|                     | Docker Compose                                     | Orchestrates multiple services (e.g., app + model + others)    |
|                     | `--device /dev/video0`                             | Grants container access to physical webcam                     |
| 🤖 Notifications    | Telegram Bot (`telebot` / `python-telegram-bot`)   | Sends real-time alerts and status updates                      |
|                     | Bot token + Chat ID                                | For secure messaging                                           |
| 📊 Logging          | `runs/detect/train*/`, `results.csv`, `labels.jpg` | YOLO training results, validation performance, and loss curves |
| 🧠 Monitoring       | TensorBoard (optional)                             | Training insights via logs (if enabled properly)               |
| ⏱️ Alert Control    | Python `time.time()`                               | Prevents alert flooding using cooldown timer                   |
| 🔗 LLM Reasoning    | LangChain                                          | Manages LLM pipeline and prompt engineering                    |
| 🤖 Prompting Agent  | Open-source LLM (e.g. Mistral via Ollama)          | Generates human-readable descriptions of detected scenes       |
---
## 📊 Model Performance Summary

| Class          | Images | Instances | Precision | Recall | mAP@0.5 | mAP@0.5:0.95 |
|----------------|--------|-----------|-----------|--------|--------|--------------|
| **all**        | 327    | 1042      | 0.645     | 0.496  | 0.528  | 0.293        |
| Armed-Person   | 260    | 376       | 0.852     | 0.522  | 0.720  | 0.436        |
| Rifle          | 274    | 405       | 0.855     | 0.306  | 0.484  | 0.220        |
| Person         | 143    | 257       | 0.575     | 0.405  | 0.468  | 0.282        |
| Knife          | 4      | 4         | 0.299     | 0.750  | 0.439  | 0.234        |

**⚡ Inference Speed**  
- Preprocess: `0.2ms`  
- Inference: `2.0ms`  
- Loss: `0.0ms`  
- Postprocess: `1.7ms`
