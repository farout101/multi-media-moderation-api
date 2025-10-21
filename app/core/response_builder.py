from fastapi.responses import JSONResponse
from datetime import datetime

def build_response(data, message="OK", error=0, status_code=200):
    payload = {
        "error": error,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": message,
        "data": data,
    }
    return JSONResponse(content=payload, status_code=status_code)

def log_event(message: str):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")
