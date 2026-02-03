import requests
import json

print('='*60)
print('FINAL COMPREHENSIVE TEST')
print('='*60)

tests = [
    {
        'name': 'Single Video (Short)',
        'url': 'https://www.youtube.com/watch?v=jNQXAC9IVRw',
        'expected_playlist': False
    },
    {
        'name': 'Playlist Detection',
        'url': 'https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf',
        'expected_playlist': True
    }
]

for test in tests:
    print(f'\n{"="*60}')
    print(f'Test: {test["name"]}')
    print(f'URL: {test["url"]}')
    print('-'*60)
    
    try:
        response = requests.post(
            'http://localhost:8000/transcript',
            json={'url': test['url']},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            is_playlist = data.get('is_playlist', False)
            
            print(f'✓ Status: {response.status_code}')
            print(f'✓ Is Playlist: {is_playlist} (expected: {test["expected_playlist"]})')
            
            if is_playlist == test['expected_playlist']:
                print(f'✓ PASS - Playlist detection correct')
            else:
                print(f'✗ FAIL - Playlist detection incorrect')
            
            if is_playlist:
                print(f'  Playlist Title: {data.get("playlist_title", "N/A")}')
                print(f'  Videos in playlist: {len(data["videos"])}')
            
            print(f'  Video count: {len(data["videos"])}')
            for i, video in enumerate(data['videos'][:2]):
                print(f'\n  Video {i+1}:')
                print(f'    Title: {video["title"][:60]}')
                print(f'    Video ID: {video["video_id"]}')
                print(f'    Source: {video["source"]}')
                print(f'    Transcript: {len(video["transcript"])} chars')
                if video["source"] != "error" and len(video["transcript"]) > 50:
                    print(f'    Preview: "{video["transcript"][:80]}..."')
        else:
            print(f'✗ FAIL - Status: {response.status_code}')
            print(f'  Response: {response.text[:200]}')
            
    except Exception as e:
        print(f'✗ ERROR: {e}')

print(f'\n{"="*60}')
print('TEST COMPLETE')
print('='*60)
