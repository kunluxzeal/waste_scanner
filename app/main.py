from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import APP_NAME, APP_VERSION
from app.routers import camera, detection, health
from app.services.camera_stream import camera_stream


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"{APP_NAME} starting...", flush=True)
    camera_stream.start()

    try:
        yield
    finally:
        camera_stream.stop()
        print(f"{APP_NAME} shutting down.", flush=True)


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="YOLO26n COCO detection using NCNN on Raspberry Pi.",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(detection.router)
app.include_router(camera.router)


@app.get("/")
def root():
    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }
