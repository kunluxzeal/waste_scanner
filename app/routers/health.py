from fastapi import APIRouter

from app.config import APP_NAME, APP_VERSION, MODEL_PATH

router = APIRouter(tags=["Health"])


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "application": APP_NAME,
        "version": APP_VERSION,
        "model_loaded": MODEL_PATH.exists(),
        "inference_backend": "NCNN",
    }
