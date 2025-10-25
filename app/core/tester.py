
import requests

def run_video_url_test(video_url, num_tests=10):
    """
    Tests the video detection URL endpoint by sending the same URL multiple times.

    Args:
        video_url (str): The URL of the video to test.
        num_tests (int): The number of times to test the video.

    Returns:
        list: A list of responses from the server.
    """
    url = "http://127.0.0.1:8000/video-detect-url"
    payload = {"url": video_url}
    results = []

    for i in range(num_tests):
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                results.append(response.json())
            else:
                results.append({"error": response.text, "status_code": response.status_code})
        except requests.exceptions.RequestException as e:
            results.append({"error": str(e)})
    
    return results
