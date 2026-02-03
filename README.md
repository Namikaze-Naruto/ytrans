# YouTube Transcript Generator

A web application that generates transcripts from YouTube videos and playlists. It automatically tries to fetch closed captions first, and falls back to audio transcription using OpenAI Whisper if captions are not available.

## Features

- **Single Video Transcription**: Get transcripts from individual YouTube videos
- **Playlist Support**: Process entire playlists and get transcripts for all videos
- **Dual Source**: Automatically uses closed captions when available, falls back to Whisper STT
- **Clean UI**: Modern, responsive interface with dark mode
- **Copy Functionality**: Copy individual or all transcripts with one click

## Requirements

- Python 3.8+
- FFmpeg (for audio extraction)
- Modern web browser

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd youtube_link_transcript
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate.bat`
   - Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Ensure FFmpeg is installed and available in your system PATH

## Usage

### Starting the Server

**Windows:**
```bash
run_server.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
python -m backend.main
```

The server will start on `http://localhost:8000`

### Using the Web Interface

1. Open `frontend/index.html` in your web browser
2. Paste a YouTube video URL or playlist URL
3. Click "Get Transcript"
4. Wait for processing (playlist may take longer)
5. Copy the transcripts as needed

## API Endpoints

### POST /transcript

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response (Single Video):**
```json
{
  "videos": [
    {
      "video_id": "VIDEO_ID",
      "title": "Video Title",
      "transcript": "Full transcript text...",
      "source": "cc"
    }
  ],
  "is_playlist": false
}
```

**Response (Playlist):**
```json
{
  "videos": [
    {
      "video_id": "VIDEO_ID_1",
      "title": "Video 1 Title",
      "transcript": "Full transcript text...",
      "source": "cc"
    },
    {
      "video_id": "VIDEO_ID_2",
      "title": "Video 2 Title",
      "transcript": "Full transcript text...",
      "source": "audio_stt"
    }
  ],
  "is_playlist": true,
  "playlist_title": "Playlist Name"
}
```

## Project Structure

```
youtube_link_transcript/
├── backend/
│   ├── main.py                 # FastAPI application
│   └── transcript_service.py   # Transcript processing logic
├── frontend/
│   ├── index.html             # Web interface
│   ├── app.js                 # Frontend logic
│   └── style.css              # Styling
├── requirements.txt           # Python dependencies
├── run_server.bat            # Windows startup script
└── README.md                 # This file
```

## How It Works

1. **URL Detection**: The system detects if the URL is a single video or playlist
2. **Closed Captions First**: Attempts to fetch existing closed captions using YouTube Transcript API
3. **Whisper Fallback**: If captions unavailable, downloads audio and transcribes using OpenAI Whisper
4. **Batch Processing**: For playlists, processes each video sequentially
5. **Results Display**: Shows all transcripts with their sources and allows individual/bulk copying

## Technologies Used

- **Backend**: FastAPI, Python
- **Transcription**: youtube-transcript-api, OpenAI Whisper
- **Audio Processing**: yt-dlp, FFmpeg
- **Frontend**: Vanilla JavaScript, HTML5, CSS3

## Notes

- First run may take longer as Whisper downloads the model
- Audio transcription is more resource-intensive than fetching captions
- Playlist processing time depends on the number of videos and transcription method used
- Temporary audio files are automatically cleaned up after transcription

## License

MIT License
