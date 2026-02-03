import os
import yt_dlp
import whisper
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import uuid
import re

# Initialize Whisper model globally to avoid reloading (lazy loading can be better but for now simpler)
# Warning: This is heavy.
# We will load it on first use or keep it loaded. Let's load on demand or global if frequently used.
# For this demo, let's load it globally but be aware of startup time.
model = None

def load_model():
    global model
    if model is None:
        print("Loading Whisper model...")
        # Use tiny model for lower memory usage on free tier hosting
        model = whisper.load_model("tiny") # tiny model uses less RAM (~1GB vs 2GB)
        print("Whisper model loaded.")
    return model

async def get_transcript(url: str):
    # Check if it's a playlist
    if is_playlist_url(url):
        return await get_playlist_transcripts(url)
    
    # Single video
    video_id = extract_video_id(url)
    transcript_data = await get_single_video_transcript(url, video_id)
    return {"videos": [transcript_data], "is_playlist": False}

async def get_single_video_transcript(url: str, video_id: str = None):
    if not video_id:
        video_id = extract_video_id(url)
    
    # Get video title
    video_title = get_video_title(url)
    
    # 1. Try fetching existing CC
    try:
        print(f"Attempting to fetch CC for {video_id}...")
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        # Formatter
        full_text = " ".join([t['text'] for t in transcript_list])
        return {"video_id": video_id, "title": video_title, "transcript": full_text, "source": "cc"}
    except (TranscriptsDisabled, NoTranscriptFound):
        print("No CC found. Falling back to Audio Download + STT.")
        pass
    except Exception as e:
        print(f"Error fetching CC: {e}")
        pass

    # 2. Fallback: Download Audio & Run Whisper
    result = await process_audio_stt(url)
    result["video_id"] = video_id
    result["title"] = video_title
    return result

def is_playlist_url(url: str):
    """Check if URL is a playlist"""
    return "list=" in url or "/playlist" in url

def extract_video_id(url: str):
    # Basic extraction, yt_dlp has better utilities but typically 'v' param or last part of path
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    return url # Fallback, might fail if standard ID not found

def get_video_title(url: str):
    """Extract video title using yt-dlp"""
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True, 'extract_flat': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('title', 'Unknown Title')
    except:
        return 'Unknown Title'

async def get_playlist_transcripts(url: str):
    """Get transcripts for all videos in a playlist"""
    print(f"Processing playlist: {url}")
    
    # Extract playlist info
    ydl_opts = {'quiet': True, 'no_warnings': True, 'extract_flat': True}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(url, download=False)
            
            if 'entries' not in playlist_info:
                raise Exception("Not a valid playlist")
            
            videos = []
            entries = playlist_info['entries']
            
            print(f"Found {len(entries)} videos in playlist")
            
            for idx, entry in enumerate(entries):
                if entry is None:
                    continue
                    
                video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                video_title = entry.get('title', f'Video {idx+1}')
                
                print(f"Processing {idx+1}/{len(entries)}: {video_title}")
                
                try:
                    result = await get_single_video_transcript(video_url, entry['id'])
                    videos.append(result)
                except Exception as e:
                    print(f"Error processing video {entry['id']}: {e}")
                    videos.append({
                        "video_id": entry['id'],
                        "title": video_title,
                        "transcript": f"Error: {str(e)}",
                        "source": "error"
                    })
            
            return {"videos": videos, "is_playlist": True, "playlist_title": playlist_info.get('title', 'Playlist')}
            
    except Exception as e:
        raise Exception(f"Failed to process playlist: {str(e)}")

async def process_audio_stt(url: str):
    # Download audio using yt-dlp
    temp_filename = f"temp_{uuid.uuid4()}.mp3"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': temp_filename.replace(".mp3", ""), # yt-dlp adds extension
        'quiet': True
    }
    
    final_filename = temp_filename # expected
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio...")
            ydl.download([url])
        
        # Check actual filename (yt-dlp might append mp3)
        if not os.path.exists(final_filename) and os.path.exists(final_filename + ".mp3"):
             final_filename += ".mp3"
        elif not os.path.exists(final_filename):
            # Try to find what it made
            pass 

        print("Audio downloaded. Transcribing...")
        m = load_model()
        result = m.transcribe(final_filename)
        
        return {"transcript": result["text"], "source": "audio_stt"}
        
    finally:
        # Cleanup
        if os.path.exists(final_filename):
            os.remove(final_filename)
        # Also check for the .mp3 version if we guessed wrong initially
        if os.path.exists(final_filename + ".mp3"):
             os.remove(final_filename + ".mp3")
