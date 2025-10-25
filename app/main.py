from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import image_router, test_multip_result, video_router
from app.core.response_builder import build_response

app = FastAPI(title="YOLOv8 Moderation API (Image + Video)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return build_response([], "healthy")

app.include_router(image_router.router)
app.include_router(video_router.router)
app.include_router(test_multip_result.router)
