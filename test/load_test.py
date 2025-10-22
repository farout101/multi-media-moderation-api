import os
import random
from locust import HttpUser, task, between

class FastAPIUser(HttpUser):
    wait_time = between(1, 3)
    test_folder = "test_videos"

    def on_start(self):
        # * Load all video file paths once
        self.video_files = [
            os.path.join(self.test_folder, f)
            for f in os.listdir(self.test_folder)
            if f.lower().endswith((".mp4", ".mov", ".avi", ".mkv"))
        ]
        if not self.video_files:
            print(f"[ERROR] No video files found in {self.test_folder}")
        else:
            print(f"[INFO] Loaded {len(self.video_files)} video files.")

    @task
    def predict_endpoint(self):
        if not self.video_files:
            return

        # * Randomly pick a file (can be changed to sequential if needed)
        video_path = random.choice(self.video_files)

        try:
            with open(video_path, "rb") as f:
                response = self.client.post("/video-detect", files={"file": f})
                if response.status_code != 200:
                    print(f"[WARN] {video_path} -> {response.status_code}")
        except Exception as e:
            print(f"[ERROR] Uploading {video_path}: {e}")
