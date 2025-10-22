# YOLO Moderation API

This is a FastAPI-based API for image and video moderation using a YOLO model.

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