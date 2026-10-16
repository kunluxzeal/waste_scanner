from pydantic import BaseModel


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class Detection(BaseModel):
    class_id: int
    class_name: str
    confidence: float
    bbox: BoundingBox


class DetectionResponse(BaseModel):
    model: str
    image_width: int
    image_height: int
    inference_time_ms: float
    detection_count: int
    detections: list[Detection]
