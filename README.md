# YOLO Moderation API

This is a FastAPI-based API for image and video moderation using a YOLOv8 model. It provides endpoints for detecting unsafe content in images and videos.

## Features

-   **Image and Video Moderation**: Detects unsafe content in images and videos.
-   **Configurable Labels**: Easily configure the labels to be considered unsafe.
-   **Load Testing**: Includes a Locust-based load testing script to evaluate performance.

## API Endpoints

The following endpoints are available:

-   `POST /image-detect`: Analyzes a single image for unsafe content.
-   `POST /video-detect`: Analyzes a video for unsafe content.
-   `GET /health`: A health check endpoint.

## Configuration

The following variables can be configured in `app/config.py`:

-   `UNSAFE_LABELS`: A set of labels to be considered unsafe.
-   `SAFE_LABELS`: A list of labels to be considered safe.
-   `YOLO_MODEL_PATH`: The path to the YOLO model file.
-   `CONFIDENCE_THRESHOLD`: The confidence threshold for object detection.
-   `IOU_THRESHOLD`: The IOU threshold for non-maximum suppression.
-   `IMG_SIZE`: The image size for model input.
-   `TEMP_DIR`: The directory for temporary media files.
-   `DEVICE`: The device to run the model on (`cuda` or `cpu`).

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/yolo-moderation-api.git
    cd yolo-moderation-api
    ```
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Place your AI model at model/ under root folder.

## Running the Application

To run the application, use the following command:

```bash
python run.py
```

The API will be available at `http://127.0.0.1:8000`.

## Load Testing with Locust

This project uses [Locust](https://locust.io/) to simulate concurrent users and test the performance of the API under load. The load test script is located at `test/load_test.py`.

### How it Works

The `load_test.py` script defines a `FastAPIUser` that sends POST requests to the `/video-detect` endpoint. It randomly selects video files from the `test_videos` directory and sends them as multipart/form-data.

### Prerequisites

1.  **Install Locust:**
    ```bash
    pip install locust
    ```
2.  **Add Test Videos:**
    Place the video files you want to use for testing in the `test_videos` directory at project root. The script will automatically discover them.

### Running the Load Test

1.  **Start the load test from the root directory of the project:**
    ```bash
    locust -f test/load_test.py
    ```
2.  **Open the Locust web interface:**
    Open your browser and go to [http://localhost:8089](http://localhost:8089).

3.  **Start the simulation:**
    -   Enter the number of users you want to simulate.
    -   Enter the spawn rate (users to start per second).
    -   Click "Start swarming".

You can then monitor the performance of the API in real-time through the Locust web interface.

## Dependencies

The project's dependencies are listed below:

-   fastapi
-   uvicorn
-   pydantic
-   Pillow
-   opencv-python
-   torch
-   ultralytics
-   python-multipart
-   locust
-   requests
-   streamlit
