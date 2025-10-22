from locust import HttpUser, task, between

class FastAPIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def predict_endpoint(self):
        # * Replace the file path with a valid path to a video file on your system
        file_path = "D:\\Code\\Projects\\VideoStreaming\\videoimg_python\\videos\\test.mp4"
        try:
            with open(file_path, "rb") as f:
                self.client.post("/video-detect", files={"file": f})
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error uploading {file_path}: {e}")
