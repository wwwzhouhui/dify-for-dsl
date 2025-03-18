from fastapi import FastAPI
from api.video import router as video_router

app = FastAPI()

# Include the video router
app.include_router(video_router, prefix="")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8085)