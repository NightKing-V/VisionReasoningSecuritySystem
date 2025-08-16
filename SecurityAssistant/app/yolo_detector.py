from ultralytics import YOLO
import numpy as np
import cv2
from PIL import Image

model = YOLO("app/yolo11n.pt")  # Make sure this model is downloaded or available


def detect_objects(image: Image.Image):
    img_array = np.array(image)
    results = model(img_array, conf=0.4, device=0)

    detections = results[0].boxes.data.cpu().numpy()
    labels = []
    annotated = img_array.copy()

    for box in detections:
        x1, y1, x2, y2, conf, cls = box
        cls = int(cls)
        label = model.names[cls]
        labels.append(label)

        # Draw box and label
        cv2.rectangle(annotated, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(annotated, label, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return list(set(labels)), Image.fromarray(annotated)
