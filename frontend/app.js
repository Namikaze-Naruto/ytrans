document.getElementById('submitBtn').addEventListener('click', async () => {
    const urlInput = document.getElementById('videoUrl');
    const resultDiv = document.getElementById('result');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    const transcriptContainer = document.getElementById('transcriptContainer');
    const loadingText = document.getElementById('loadingText');
    const resultTitle = document.getElementById('resultTitle');

    const url = urlInput.value.trim();
    if (!url) return;

    // Reset state
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    loadingDiv.classList.remove('hidden');
    transcriptContainer.innerHTML = '';

    try {
        const response = await fetch('http://localhost:8000/transcript', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Failed to fetch transcript');
        }

        const data = await response.json();

        // Handle playlist or single video
        if (data.is_playlist) {
            resultTitle.textContent = `Playlist: ${data.playlist_title || 'Results'}`;
            loadingText.textContent = `Processing playlist (${data.videos.length} videos)...`;
            
            data.videos.forEach((video, index) => {
                const videoDiv = document.createElement('div');
                videoDiv.className = 'video-transcript';
                
                const header = document.createElement('div');
                header.className = 'video-header';
                header.innerHTML = `
                    <h3>${index + 1}. ${video.title}</h3>
                    <div>
                        <span class="badge">${getSourceLabel(video.source)}</span>
                        <button class="copy-video-btn secondary-btn" data-index="${index}">Copy</button>
                    </div>
                `;
                
                const content = document.createElement('div');
                content.className = 'transcript-box';
                content.textContent = video.transcript;
                
                videoDiv.appendChild(header);
                videoDiv.appendChild(content);
                transcriptContainer.appendChild(videoDiv);
            });
        } else {
            // Single video
            const video = data.videos[0];
            resultTitle.textContent = video.title;
            
            const videoDiv = document.createElement('div');
            videoDiv.className = 'video-transcript';
            
            const header = document.createElement('div');
            header.className = 'video-header';
            header.innerHTML = `
                <span class="badge">${getSourceLabel(video.source)}</span>
            `;
            
            const content = document.createElement('div');
            content.className = 'transcript-box';
            content.textContent = video.transcript;
            
            videoDiv.appendChild(header);
            videoDiv.appendChild(content);
            transcriptContainer.appendChild(videoDiv);
        }

        resultDiv.classList.remove('hidden');
        
        // Add event listeners to copy buttons
        document.querySelectorAll('.copy-video-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const index = e.target.dataset.index;
                const transcript = data.videos[index].transcript;
                copyToClipboard(transcript, e.target);
            });
        });
        
    } catch (err) {
        errorDiv.textContent = err.message;
        errorDiv.classList.remove('hidden');
    } finally {
        loadingDiv.classList.add('hidden');
    }
});

document.getElementById('copyAllBtn').addEventListener('click', () => {
    const transcripts = Array.from(document.querySelectorAll('.transcript-box'))
        .map(box => box.textContent)
        .join('\n\n---\n\n');
    copyToClipboard(transcripts, document.getElementById('copyAllBtn'));
});

function getSourceLabel(source) {
    switch(source) {
        case 'cc': return 'Source: Closed Captions';
        case 'audio_stt': return 'Source: Audio Transcription (Whisper)';
        case 'error': return 'Error';
        default: return 'Source: Unknown';
    }
}

function copyToClipboard(text, button) {
    navigator.clipboard.writeText(text).then(() => {
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        setTimeout(() => button.textContent = originalText, 2000);
    });
}
