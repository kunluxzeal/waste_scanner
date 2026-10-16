from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "yolo26n_ncnn_model"

IMAGE_SIZE = 320
CONFIDENCE_THRESHOLD = 0.25
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB
APP_NAME = "YOLO26 Object Detection API"
APP_VERSION = "1.0.0"
