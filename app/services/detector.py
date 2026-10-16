import time

import cv2
import numpy as np
from ultralytics import YOLO

from app.config import MODEL_PATH, IMAGE_SIZE, CONFIDENCE_THRESHOLD


class ObjectDetector:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"NCNN model not found: {MODEL_PATH}"
            )

        print(f"Loading NCNN model: {MODEL_PATH}", flush=True)
        self.model = YOLO(str(MODEL_PATH))
        print("NCNN model loaded successfully.", flush=True)

    def detect(self, image: np.ndarray) -> dict:
        height, width = image.shape[:2]
        start_time = time.perf_counter()

        results = self.model.predict(
            source=image,
            imgsz=IMAGE_SIZE,
            conf=CONFIDENCE_THRESHOLD,
            device="cpu",
            verbose=False,
        )

        elapsed_ms = (time.perf_counter() - start_time) * 1000
        result = results[0]
        detections = []

        for box in result.boxes:
            class_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detections.append({
                "class_id": class_id,
                "class_name": self.model.names[class_id],
                "confidence": round(confidence, 4),
                "bbox": {
                    "x1": round(float(x1), 2),
                    "y1": round(float(y1), 2),
                    "x2": round(float(x2), 2),
                    "y2": round(float(y2), 2),
                },
            })

        return {
            "model": "YOLO26n-NCNN",
            "image_width": width,
            "image_height": height,
            "inference_time_ms": round(elapsed_ms, 2),
            "detection_count": len(detections),
            "detections": detections,
        }


detector = ObjectDetector()
