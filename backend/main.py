from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from backend.transcript_service import get_transcript
import os


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (frontend)
app.mount("/static", StaticFiles(directory="frontend"), name="static")


class TranscriptRequest(BaseModel):
    url: str

class VideoTranscript(BaseModel):
    video_id: str
    title: str
    transcript: str
    source: str # 'cc', 'audio_stt', or 'error'

class TranscriptResponse(BaseModel):
    videos: List[VideoTranscript]
    is_playlist: bool
    playlist_title: Optional[str] = None

@app.get("/")
async def read_root():
    """Serve the frontend"""
    return FileResponse('frontend/index.html')

@app.post("/transcript")
async def generate_transcript(request: TranscriptRequest):
    try:
        transcript_data = await get_transcript(request.url)
        return transcript_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
