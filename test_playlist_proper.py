import requests
import json

print('='*60)
print('Testing PLAYLIST with proper playlist URL')
print('='*60)

# Use proper playlist URL format
playlist_url = 'https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf'

print(f'\nSending request to: http://localhost:8000/transcript')
print(f'Playlist URL: {playlist_url}')

try:
    response = requests.post(
        'http://localhost:8000/transcript',
        json={'url': playlist_url},
        timeout=180
    )
    
    print(f'\nStatus Code: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        print(f'\n✓ SUCCESS!')
        print(f'  Is Playlist: {data["is_playlist"]}')
        print(f'  Playlist Title: {data.get("playlist_title", "N/A")}')
        print(f'  Number of videos: {len(data["videos"])}')
        print(f'\n  Videos processed:')
        
        for i, video in enumerate(data['videos']):
            print(f'    {i+1}. {video["title"][:60]}')
            print(f'       Source: {video["source"]}, Length: {len(video["transcript"])} chars')
            if len(video["transcript"]) < 200:
                print(f'       Preview: {video["transcript"][:100]}')
    else:
        print(f'\n✗ FAILED with status {response.status_code}')
        print(response.text)
        
except Exception as e:
    print(f'\n✗ ERROR: {e}')
