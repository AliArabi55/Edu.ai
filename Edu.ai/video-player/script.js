class VideoPlayer {
    constructor() {
        this.video = document.getElementById('courseVideo');
        this.startOverlay = document.getElementById('startOverlay');
        this.startButton = document.getElementById('startButton');
        this.videoControls = document.getElementById('videoControls');
        this.endScreen = document.getElementById('endScreen');
        this.playPauseBtn = document.getElementById('playPauseBtn');
        this.progress = document.getElementById('progress');
        this.currentTimeDisplay = document.getElementById('currentTime');
        this.totalTimeDisplay = document.getElementById('totalTime');
        this.volumeBtn = document.getElementById('volumeBtn');
        this.fullscreenBtn = document.getElementById('fullscreenBtn');
        this.speedSelect = document.getElementById('speedSelect');
        
        this.isPlaying = false;
        this.videoEnded = false;
        
        this.initializeEventListeners();
        this.loadVideoMetadata();
    }
    
    initializeEventListeners() {
        // Start button click
        this.startButton.addEventListener('click', () => this.startVideo());
        
        // Video events
        this.video.addEventListener('loadedmetadata', () => this.updateTotalTime());
        this.video.addEventListener('timeupdate', () => this.updateProgress());
        this.video.addEventListener('ended', () => this.onVideoEnd());
        this.video.addEventListener('play', () => this.onPlay());
        this.video.addEventListener('pause', () => this.onPause());
        
        // Control buttons
        this.playPauseBtn.addEventListener('click', () => this.togglePlayPause());
        this.volumeBtn.addEventListener('click', () => this.toggleMute());
        this.fullscreenBtn.addEventListener('click', () => this.toggleFullscreen());
        this.speedSelect.addEventListener('change', () => this.changeSpeed());
        
        // Progress bar click
        document.querySelector('.progress-bar').addEventListener('click', (e) => this.seek(e));
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
        
        // Video container hover for controls
        document.getElementById('videoContainer').addEventListener('mouseenter', () => this.showControls());
        document.getElementById('videoContainer').addEventListener('mouseleave', () => this.hideControls());
    }
    
    loadVideoMetadata() {
        if (this.video.readyState >= 1) {
            this.updateTotalTime();
        }
    }
    
    startVideo() {
        // Hide start overlay
        this.startOverlay.style.display = 'none';
        
        // Show video controls
        this.videoControls.style.display = 'block';
        
        // Set playback speed to 1.5x
        this.video.playbackRate = 1.5;
        
        // Start playing
        this.video.play();
        
        // Add analytics or tracking here if needed
        this.trackVideoStart();
    }
    
    togglePlayPause() {
        if (this.video.paused) {
            this.video.play();
        } else {
            this.video.pause();
        }
    }
    
    onPlay() {
        this.isPlaying = true;
        this.updatePlayPauseIcon('pause');
    }
    
    onPause() {
        this.isPlaying = false;
        this.updatePlayPauseIcon('play');
    }
    
    updatePlayPauseIcon(state) {
        const icon = this.playPauseBtn.querySelector('svg path');
        if (state === 'play') {
            icon.setAttribute('d', 'M8 5v14l11-7z'); // Play icon
        } else {
            icon.setAttribute('d', 'M6 19h4V5H6v14zm8-14v14h4V5h-4z'); // Pause icon
        }
    }
    
    updateProgress() {
        if (this.video.duration) {
            const progressPercent = (this.video.currentTime / this.video.duration) * 100;
            this.progress.style.width = progressPercent + '%';
            
            // Update current time display
            this.currentTimeDisplay.textContent = this.formatTime(this.video.currentTime);
        }
    }
    
    updateTotalTime() {
        if (this.video.duration) {
            this.totalTimeDisplay.textContent = this.formatTime(this.video.duration);
        }
    }
    
    formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
    
    seek(e) {
        const progressBar = e.currentTarget;
        const rect = progressBar.getBoundingClientRect();
        const percent = (e.clientX - rect.left) / rect.width;
        this.video.currentTime = percent * this.video.duration;
    }
    
    toggleMute() {
        this.video.muted = !this.video.muted;
        this.updateVolumeIcon();
    }
    
    updateVolumeIcon() {
        const icon = this.volumeBtn.querySelector('svg path');
        if (this.video.muted) {
            icon.setAttribute('d', 'M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z'); // Muted icon
        } else {
            icon.setAttribute('d', 'M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z'); // Volume icon
        }
    }
    
    toggleFullscreen() {
        const container = document.getElementById('videoContainer');
        if (!document.fullscreenElement) {
            container.requestFullscreen().catch(err => {
                console.log(`Error attempting to enable fullscreen: ${err.message}`);
            });
        } else {
            document.exitFullscreen();
        }
    }
    
    changeSpeed() {
        const speed = parseFloat(this.speedSelect.value);
        this.video.playbackRate = speed;
        console.log(`Video speed changed to: ${speed}x`);
    }
    
    showControls() {
        if (this.isPlaying) {
            this.videoControls.style.opacity = '1';
        }
    }
    
    hideControls() {
        if (this.isPlaying) {
            setTimeout(() => {
                this.videoControls.style.opacity = '0.7';
            }, 1000);
        }
    }
    
    handleKeyboard(e) {
        // Only handle keyboard events when video is playing
        if (this.startOverlay.style.display !== 'none') return;
        
        switch(e.code) {
            case 'Space':
                e.preventDefault();
                this.togglePlayPause();
                break;
            case 'KeyM':
                this.toggleMute();
                break;
            case 'KeyF':
                this.toggleFullscreen();
                break;
            case 'ArrowLeft':
                e.preventDefault();
                this.video.currentTime = Math.max(0, this.video.currentTime - 10);
                break;
            case 'ArrowRight':
                e.preventDefault();
                this.video.currentTime = Math.min(this.video.duration, this.video.currentTime + 10);
                break;
        }
    }
    
    onVideoEnd() {
        this.videoEnded = true;
        this.isPlaying = false;
        this.videoControls.style.display = 'none';
        this.endScreen.style.display = 'flex';
        
        // Add completion tracking
        this.trackVideoCompletion();
        
        // Auto-advance after delay (optional)
        setTimeout(() => {
            this.showNextLessonPrompt();
        }, 3000);
    }
    
    trackVideoStart() {
        // Analytics tracking for video start
        console.log('Video started:', new Date());
        // You can add Google Analytics or other tracking here
    }
    
    trackVideoCompletion() {
        // Analytics tracking for video completion
        console.log('Video completed:', new Date());
        // You can add completion analytics here
        
        // Store completion in localStorage
        localStorage.setItem('machine_learning_video_completed', 'true');
        localStorage.setItem('machine_learning_completion_date', new Date().toISOString());
    }
    
    showNextLessonPrompt() {
        // Optional: show a subtle prompt for next action
        console.log('Ready for next action');
    }
}

// Global functions for end screen buttons
function goToNextLesson() {
    // Navigate to quiz or next lesson
    window.location.href = '../7.Quiz 1/index.html';
}

function replayVideo() {
    const player = window.videoPlayer;
    if (player) {
        player.video.currentTime = 0;
        player.endScreen.style.display = 'none';
        player.startOverlay.style.display = 'flex';
        player.videoEnded = false;
    }
}

function backToCourses() {
    window.location.href = '../5.courses/index.html';
}

// Initialize video player when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.videoPlayer = new VideoPlayer();
    
    // Preload video for better performance
    const video = document.getElementById('courseVideo');
    video.preload = 'metadata';
    
    // Add loading indicator
    video.addEventListener('loadstart', () => {
        console.log('Video loading started');
    });
    
    video.addEventListener('canplaythrough', () => {
        console.log('Video ready to play');
    });
});

// Handle page visibility changes (pause when tab is hidden)
document.addEventListener('visibilitychange', () => {
    const player = window.videoPlayer;
    if (player && player.isPlaying) {
        if (document.hidden) {
            player.video.pause();
        }
    }
});