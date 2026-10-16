import cv2
import numpy as np

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import MAX_UPLOAD_SIZE
from app.schemas.detection import DetectionResponse
from app.services.detector import detector

router = APIRouter(
    prefix="/api/v1",
    tags=["Object Detection"],
)


@router.post("/detect", response_model=DetectionResponse)
def detect_objects(file: UploadFile = File(...)):
    contents = file.file.read(MAX_UPLOAD_SIZE + 1)

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    if len(contents) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Image exceeds the 10 MB upload limit.",
        )

    encoded_image = np.frombuffer(contents, dtype=np.uint8)
    image = cv2.imdecode(encoded_image, cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid image. Upload a supported image file.",
        )

    try:
        return detector.detect(image)
    except Exception as exc:
        print(f"Detection error: {exc}", flush=True)
        raise HTTPException(
            status_code=500,
            detail="Object detection failed.",
        ) from exc
