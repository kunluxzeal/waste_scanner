import threading
import time
import traceback

import torch
from app.services.detector import detector

import cv2
from picamera2 import Picamera2

class CameraStream:
    def __init__(self):
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread = None
        self._latest_jpeg = None
        self._running = False
        self._last_error = None
        self._inference_time_ms = 0.0
        self._fps = 0.0

    def start(self):
        if self._thread is not None and self._thread.is_alive():
            return

        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run,
            name="camera-detection-worker",
            daemon=True,
        )
        self._thread.start()

    def stop(self):
        self._stop_event.set()

        if self._thread is not None:
            self._thread.join(timeout=10)

    def _run(self):
        camera = None

        try:
            camera = Picamera2()
            config = camera.create_video_configuration(
                main={"size": (640, 480), "format": "RGB888"},
                buffer_count=4,
            )
            camera.configure(config)
            camera.start()
            time.sleep(1)

            with self._lock:
                self._running = True
                self._last_error = None

            print("CSI camera started at 640x480", flush=True)
            previous_time = time.perf_counter()

            while not self._stop_event.is_set():
                frame = camera.capture_array("main")

                started = time.perf_counter()
                results = detector.model.predict(
                    source=frame,
                    imgsz=320,
                    conf=0.25,
                    device="cpu",
                    verbose=False,
                )
                inference_ms = (time.perf_counter() - started) * 1000

                # Ultralytics draws bounding boxes and class labels.
                annotated = results[0].plot()

                ok, encoded = cv2.imencode(
                    ".jpg",
                    annotated,
                    [cv2.IMWRITE_JPEG_QUALITY, 80],
                )

                now = time.perf_counter()
                elapsed = now - previous_time
                previous_time = now
                fps = 1.0 / elapsed if elapsed > 0 else 0.0

                if ok:
                    with self._lock:
                        self._latest_jpeg = encoded.tobytes()
                        self._inference_time_ms = round(inference_ms, 2)
                        self._fps = round(fps, 2)
                        self._last_error = None

        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            print(f"Camera worker error: {error}", flush=True)
            traceback.print_exc()

            with self._lock:
                self._last_error = error
                self._running = False

        finally:
            if camera is not None:
                try:
                    camera.stop()
                except Exception:
                    pass
                try:
                    camera.close()
                except Exception:
                    pass

            with self._lock:
                self._running = False

            print("Camera worker stopped", flush=True)

    def get_frame(self):
        with self._lock:
            return self._latest_jpeg

    def get_status(self):
        with self._lock:
            return {
                "camera_running": self._running,
                "frame_available": self._latest_jpeg is not None,
                "inference_time_ms": self._inference_time_ms,
                "capture_fps": self._fps,
                "error": self._last_error,
            }


camera_stream = CameraStream()
