import requests
import json

print('='*60)
print('Testing with YouTube official channel playlist')
print('='*60)

# Try a public YouTube playlist that should work
# This is a short playlist from YouTube Creators
playlist_url = 'https://www.youtube.com/playlist?list=PLiCvVJzBupKmEehQ3hnNbbfBjLUyvGlqx'

print(f'\nSending request to: http://localhost:8000/transcript')
print(f'Testing with official playlist...')
print('(This may take 2-3 minutes for multiple videos)')

try:
    response = requests.post(
        'http://localhost:8000/transcript',
        json={'url': playlist_url},
        timeout=300
    )
    
    print(f'\n✓ Status Code: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        print(f'\n✓✓ PLAYLIST TEST PASSED!')
        print(f'  Is Playlist: {data["is_playlist"]}')
        print(f'  Playlist Title: {data.get("playlist_title", "N/A")}')
        print(f'  Number of videos: {len(data["videos"])}')
        print(f'\n  Results:')
        
        for i, video in enumerate(data['videos'][:5]):  # Show first 5
            print(f'\n    [{i+1}] {video["title"][:70]}')
            print(f'        Video ID: {video["video_id"]}')
            print(f'        Source: {video["source"]}')
            print(f'        Transcript length: {len(video["transcript"])} chars')
            if video["source"] != "error":
                print(f'        First 100 chars: {video["transcript"][:100]}...')
    else:
        print(f'\n✗ FAILED with status {response.status_code}')
        print(response.text)
        
except Exception as e:
    print(f'\n✗ ERROR: {e}')
