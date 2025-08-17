import cv2
from ultralytics import YOLO
import time
from collections import defaultdict
from telegrambot import send_telegram_alert
from llm_agent import analyze_scene 

model_path = "app/best.pt"

class ThreatDetectionModel:
    def __init__(self, model_path=model_path, target_classes=None, alert_cooldown=20, detection_window=50, min_detections=60):
        self.model = YOLO(model_path)
        self.target_classes = target_classes or ['Armed-Person', 'Rifle', 'knife']
        self.last_alert_time = 0
        self.alert_cooldown = alert_cooldown
        self.detection_window = detection_window
        self.min_detections = min_detections
        self.detection_history = defaultdict(list)

    def infer(self, frame, send_alert=True):
        results = self.model(frame, stream=True)
        current_detections = set()
        now = time.time()

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                name = self.model.names[cls_id]

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{name} {conf:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                if name in self.target_classes:
                    current_detections.add(name)
                    self.detection_history[name].append(now)

        # Clean old detections
        for cls_name in list(self.detection_history.keys()):
            self.detection_history[cls_name] = [
                t for t in self.detection_history[cls_name] if now - t <= self.detection_window
            ]

        # Alert logic with LLM
        if send_alert:
            triggered_threats = [
                cls_name for cls_name, timestamps in self.detection_history.items()
                if len(timestamps) >= self.min_detections
            ]

            if triggered_threats and (now - self.last_alert_time > self.alert_cooldown):
                llm_summary = analyze_scene(triggered_threats)
                send_telegram_alert(triggered_threats, llm_summary)
                self.last_alert_time = now
                self.detection_history.clear()

        return frame, current_detections
