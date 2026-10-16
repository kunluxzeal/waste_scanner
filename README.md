#  AI-Powered Electronic Waste Scanner

YoloSort is a hardware-based electronic waste scanning system that uses YOLO object detection to identify and classify electronic waste items. The system integrates a computer vision model with a FastAPI backend to process images and return detection results for display on a user interface.

Designed for deployment on a Raspberry Pi 4, YoloSort demonstrates how edge AI and embedded systems can support electronic waste identification, recycling awareness, and responsible disposal.

## Features

- **YOLO Object Detection:** Identifies and classifies supported objects in camera images.
- **FastAPI Backend:** Provides REST API endpoints for image processing and AI inference.
- **Raspberry Pi Deployment:** Designed for edge AI inference on Raspberry Pi hardware.
- **Image-Based Detection:** Accepts images for object detection and classification.
- **Detection Results:** Returns detected object classes, confidence scores, and bounding-box coordinates when provided by the model.
- **Frontend Integration:** Supports integration with a web-based interface for displaying scanning results.
- **Local Inference:** Designed to run AI inference on the device without requiring a cloud-based inference service.

## System Architecture

The system follows this workflow:

1. An image is captured using a camera or supplied through the application.
2. The image is sent to the FastAPI backend.
3. The YOLO model processes the image and detects supported objects.
4. The backend formats the detection results into an API response.
5. The frontend displays the detected objects and their confidence scores.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Backend framework | FastAPI |
| AI model | Ultralytics YOLO |
| Computer vision | OpenCV, where required |
| API server | Uvicorn |
| Deployment hardware | Raspberry Pi 4 |
| API testing | Postman |
| Version control | Git and GitHub |

## Project Structure

```text
yolo_fastapi/
├── main.py                  # FastAPI application entry point
├── requirements.txt         # Python dependencies
├── .gitignore               # Excluded files and directories
├── models/
│   └── yolo26n.pt           # YOLO model weights (if included)
├── outputs/                 # Generated detection outputs (if used)
└── README.md                # Project documentation
```

The structure above is illustrative. Update the filenames and directories to match the actual project.

## Hardware Requirements

- Raspberry Pi 4
- Raspberry Pi OS or another compatible Linux distribution
- MicroSD card or storage device with sufficient free space
- Camera module or another supported image input source
- Stable power supply
- Network connection for installation and API access

## Software Requirements

- Python 3.11 or another Python version supported by your dependencies
- pip
- Git
- FastAPI
- Uvicorn
- Ultralytics YOLO and its required inference dependencies

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/kunluxzeal/waste_scanner.git
cd waste_scanner
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If your system does not have the required Python virtual environment package, install it using your operating system's package manager.

### 3. Install dependencies

If `requirements.txt` is available:

```bash
pip install -r requirements.txt
```

Ensure the installed PyTorch, Ultralytics, and other dependencies are compatible with your Raspberry Pi's ARM64 architecture.

### 4. Configure the YOLO model

Place the required model weights in the configured model directory.

For example:

```text
models/yolo26n.pt
```

The filename and path must match those specified in your backend code.

If the model weights are not included in the repository, obtain them from the appropriate official source or your model-export workflow. Do not commit your virtual environment or large generated model exports to GitHub.

## Running the Backend

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Start the FastAPI application using the actual Python module containing your application instance.

For example, if your application is defined in `main.py` as `app`:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be accessible on port `8000` of the Raspberry Pi.

To access the interactive API documentation, open:

```text
http://<RASPBERRY_PI_IP>:8000/docs
```

Replace `<RASPBERRY_PI_IP>` with the Raspberry Pi's IP address. Access from another device requires both devices to be able to communicate over the network and the relevant port to be accessible.

## API Documentation

FastAPI provides interactive documentation at `/docs` and an alternative documentation interface at `/redoc`, provided these routes are enabled.

The actual application endpoints depend on the backend implementation. Document each endpoint using the following format:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check, if implemented |
| POST | `/predict` | Image-based object detection, if implemented |
| GET | `/docs` | Interactive API documentation |
| GET | `/redoc` | Alternative API documentation |

Use the interactive documentation to inspect the actual request formats, response schemas, and available endpoints.

## Testing with Postman

1. Start the FastAPI backend.
2. Open Postman.
3. Enter the appropriate endpoint URL, such as `http://<RASPBERRY_PI_IP>:8000/predict`, if `/predict` is implemented.
4. Select the HTTP method specified by the endpoint.
5. Configure the request body according to the backend's expected image-upload format.
6. Send the request and inspect the returned detections.

A successful inference response should contain the fields defined by the application, potentially including detected classes, confidence scores, and bounding-box coordinates.

## Git Ignore and Model Management

The repository should exclude local development environments, generated files, and secrets.

Example `.gitignore` rules:

```gitignore
# Python environments
.venv/
venv/
yolo_export_env/

# Python cache
__pycache__/
*.py[cod]
.pytest_cache/

# Secrets
.env
.env.*

# Logs
*.log

# Generated output
outputs/

# Model weights and exports
models/*.pt
models/*_ncnn_model/

# Frontend dependencies
node_modules/
frontend/node_modules/
frontend/dist/

# Editor files
.vscode/
.idea/
.DS_Store
```

**Important:** The model exclusions above are appropriate only if you intend to keep the model weights out of GitHub. Document how to obtain the model so the application can be reproduced.

If a virtual environment was already staged, remove it from Git's index without deleting the local files:

```bash
git rm -r --cached --ignore-unmatch yolo_export_env
```

Then check the staged changes before committing.

## Security Considerations

- Never commit API keys, passwords, or private configuration files.
- Avoid exposing the development server directly to the public internet.
- Restrict access to the API when deploying outside a trusted local network.
- Keep Python dependencies and system packages updated.

## Future Improvements

- Improve detection accuracy for supported electronic waste categories.
- Integrate a live camera preview and scanning interface.
- Optimize model inference for Raspberry Pi hardware.
- Add scan history and structured detection logging.
- Integrate the scanner with a database or recycling information service.
- Add clearer disposal guidance for identified electronic waste.

## Project Goal

EcoSort aims to demonstrate the practical application of computer vision, edge AI, and embedded computing in electronic waste identification. By providing a hardware-based scanning interface and AI-powered detection results, the system can support more informed recycling and disposal decisions.

## Author

**Kunle Olujimi**

Embedded Systems & Edge AI Engineer

GitHub: [@kunluxzeal](https://github.com/kunluxzeal)
