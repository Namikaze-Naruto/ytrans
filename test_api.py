import requests
import json

# Test single video
print("Testing single video...")
response = requests.post(
    'http://localhost:8000/transcript',
    json={'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
)

if response.status_code == 200:
    data = response.json()
    print(f"✓ Single video test passed")
    print(f"  Title: {data['videos'][0]['title']}")
    print(f"  Source: {data['videos'][0]['source']}")
    print(f"  Transcript length: {len(data['videos'][0]['transcript'])} chars")
else:
    print(f"✗ Single video test failed: {response.status_code}")
    print(response.text)

print("\n" + "="*50 + "\n")

# Test playlist (small playlist for quick test)
print("Testing playlist...")
response = requests.post(
    'http://localhost:8000/transcript',
    json={'url': 'https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf'}
)

if response.status_code == 200:
    data = response.json()
    print(f"✓ Playlist test passed")
    print(f"  Is playlist: {data['is_playlist']}")
    print(f"  Playlist title: {data.get('playlist_title', 'N/A')}")
    print(f"  Number of videos: {len(data['videos'])}")
    for i, video in enumerate(data['videos'][:3]):  # Show first 3
        print(f"  Video {i+1}: {video['title']} ({video['source']})")
else:
    print(f"✗ Playlist test failed: {response.status_code}")
    print(response.text)
