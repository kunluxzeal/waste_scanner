import time

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, StreamingResponse

from app.services.camera_stream import camera_stream

router = APIRouter(prefix="/api/v1/camera", tags=["Live Camera"])


@router.get("/status")
def camera_status():
    return camera_stream.get_status()


@router.get("/snapshot")
def camera_snapshot():
    frame = camera_stream.get_frame()

    if frame is None:
        status = camera_stream.get_status()
        detail = status["error"] or "Waiting for the first camera frame."
        raise HTTPException(status_code=503, detail=detail)

    return Response(
        content=frame,
        media_type="image/jpeg",
        headers={"Cache-Control": "no-store"},
    )


def generate_mjpeg():
    while True:
        frame = camera_stream.get_frame()

        if frame is not None:
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n"
                b"Cache-Control: no-store\r\n\r\n"
                + frame
                + b"\r\n"
            )
        else:
            status = camera_stream.get_status()
            if status["error"]:
                return

        time.sleep(0.03)


@router.get("/stream")
def camera_mjpeg_stream():
    return StreamingResponse(
        generate_mjpeg(),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
