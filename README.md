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

## Testing the Application under load
Make sure you have locust installed in your system:
```bash
pip install locust
```
*Make Sure You Have Pointed The Correcet Video Path in load_test.py*
To test the application, use the following command:

```bash
locust -f test/load_test.py
```