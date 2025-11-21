document.addEventListener('DOMContentLoaded', () => {
    const videoFeed = document.getElementById('video-feed');
    const streamBtn = document.getElementById('stream-btn');
    const responseText = document.getElementById('response-text');
    const responseHistory = document.getElementById('response-history');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    const yoshiOverlay = document.getElementById('yoshi-overlay');

    let isStreaming = false;
    let ws;
    let streamInterval;
    const maxHistory = 10;

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            videoFeed.srcObject = stream;
        })
        .catch(err => {
            console.error("Error accessing camera: ", err);
            responseText.textContent = "Error: Could not access camera.";
        });
    
    streamBtn.addEventListener('click', () => {
        if (!isStreaming) {
            startStreaming();
        } else {
            stopStreaming();
        }
    });

    function startStreaming() {
        ws = new WebSocket(`ws://${window.location.host}/ws`);
        
        ws.onopen = () => {
            console.log("WebSocket connection established");
            isStreaming = true;
            streamBtn.textContent = "Stop Streaming";
            streamBtn.classList.remove('btn-success');
            streamBtn.classList.add('btn-danger');

            streamInterval = setInterval(() => {
                canvas.width = videoFeed.videoWidth;
                canvas.height = videoFeed.videoHeight;
                context.drawImage(videoFeed, 0, 0, canvas.width, canvas.height);
                const data = canvas.toDataURL('image/jpeg');
                ws.send(data);
            }, 1000); // Send a frame every second
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            responseText.textContent = data.description;
            
            if (data.yoshi_found) {
                yoshiOverlay.style.display = 'flex';
            } else {
                yoshiOverlay.style.display = 'none';
            }

            // Add to history
            const newHistoryItem = document.createElement('p');
            const now = new Date();
            const timestamp = now.toLocaleTimeString();
            newHistoryItem.textContent = `[${timestamp}] ${data.description}`;
            responseHistory.prepend(newHistoryItem);

            // Limit history
            if (responseHistory.children.length > maxHistory) {
                responseHistory.removeChild(responseHistory.lastChild);
            }
        };

        ws.onclose = () => {
            console.log("WebSocket connection closed");
            stopStreaming();
        };

        ws.onerror = (error) => {
            console.error("WebSocket error: ", error);
            responseText.textContent = "An error occurred with the connection.";
            stopStreaming();
        };
    }

    function stopStreaming() {
        if (streamInterval) {
            clearInterval(streamInterval);
            streamInterval = null;
        }
        if (ws) {
            ws.close();
            ws = null;
        }
        isStreaming = false;
        streamBtn.textContent = "Start Streaming";
        streamBtn.classList.remove('btn-danger');
        streamBtn.classList.add('btn-success');
        yoshiOverlay.style.display = 'none';
    }
});
