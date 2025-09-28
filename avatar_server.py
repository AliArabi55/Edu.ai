#!/usr/bin/env python3
"""
Edu.ai Avatar Web Server
Provides a web interface to launch and control the Avatar assistant automatically
Now includes TTS Avatar video generation functionality
"""

import os
import sys
import subprocess
import signal
import threading
import time
import json
import uuid
import requests
from pathlib import Path
from flask import Flask, request, jsonify, render_template_string, send_file
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variable to track Avatar process
avatar_process = None
avatar_thread = None

def setup_environment():
    """Setup environment variables for Avatar"""
    project_root = Path(__file__).parent
    env_file = project_root / '.env'
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    
    # Check if required keys are set
    required_keys = ['AZURE_VOICELIVE_ENDPOINT', 'AZURE_VOICELIVE_API_KEY']
    missing_keys = [key for key in required_keys if not os.environ.get(key) or os.environ.get(key).strip() == '']
    
    if missing_keys:
        logger.error("❌ Missing required Azure keys!")
        logger.error("Please set up your .env file with your Azure OpenAI credentials")
        logger.error("See .env.example for template")
        return False
    
    return True

def run_avatar_process():
    """Run Avatar.py in a separate process"""
    global avatar_process
    
    avatar_dir = Path(__file__).parent / "Edu.ai" / "6.2"
    avatar_script = avatar_dir / "Avatar.py"
    
    if not avatar_script.exists():
        logger.error(f"Avatar.py not found at {avatar_script}")
        return False
    
    # Setup environment and check keys
    if not setup_environment():
        logger.error("Cannot start Avatar: Missing Azure credentials")
        return False
    
    endpoint = os.environ.get('AZURE_VOICELIVE_ENDPOINT', '')
    api_key = os.environ.get('AZURE_VOICELIVE_API_KEY', '')
    
    if not endpoint or not api_key:
        logger.error("❌ Azure credentials not configured properly")
        return False
    
    # Build command
    cmd = [
        sys.executable,
        str(avatar_script),
        "--endpoint", endpoint,
        "--api-key", api_key,
        "--model", "gpt-4o-realtime-preview",
        "--voice", "alloy"
    ]
    
    try:
        # Change to Avatar directory
        os.chdir(avatar_dir)
        
        # Start Avatar process
        avatar_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        logger.info(f"Started Avatar process with PID: {avatar_process.pid}")
        
        # Wait for process to complete
        stdout, stderr = avatar_process.communicate()
        
        if avatar_process.returncode == 0:
            logger.info("Avatar completed successfully")
        else:
            logger.error(f"Avatar failed with return code: {avatar_process.returncode}")
            logger.error(f"Error output: {stderr}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error starting Avatar: {e}")
        return False

@app.route('/')
def index():
    """Main page with Avatar control"""
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Edu.ai Avatar Control</title>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        .btn {
            background: #4CAF50;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px;
        }
        .btn:hover {
            background: #45a049;
        }
        .btn:disabled {
            background: #cccccc;
            cursor: not-allowed;
        }
        .status {
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
            background: rgba(255,255,255,0.2);
        }
        .avatar-display {
            width: 250px;
            height: 250px;
            border-radius: 50%;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
            background-size: 300% 300%;
            margin: 20px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 5em;
            animation: gradientShift 3s ease infinite, breathe 2s ease-in-out infinite;
            position: relative;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .avatar-display::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #ff6b6b);
            background-size: 400% 400%;
            border-radius: 50%;
            z-index: -1;
            animation: borderGlow 2s linear infinite;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes breathe {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        @keyframes borderGlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .speaking {
            animation: speak 0.3s infinite alternate, gradientShift 1s ease infinite, breathe 1s ease-in-out infinite;
            transform: scale(1.1);
        }
        
        @keyframes speak {
            0% { 
                transform: scale(1.1) rotate(-2deg);
                filter: hue-rotate(0deg);
            }
            100% { 
                transform: scale(1.15) rotate(2deg);
                filter: hue-rotate(30deg);
            }
        }
        
        .thinking {
            animation: think 1s ease-in-out infinite, gradientShift 1.5s ease infinite;
        }
        
        @keyframes think {
            0%, 100% { 
                transform: scale(1) rotate(0deg);
                filter: brightness(1);
            }
            25% { 
                transform: scale(1.02) rotate(-1deg);
                filter: brightness(1.1);
            }
            75% { 
                transform: scale(1.02) rotate(1deg);
                filter: brightness(0.9);
            }
        }
        
        .idle {
            animation: breathe 3s ease-in-out infinite, gradientShift 4s ease infinite;
        }
        
        @keyframes listen {
            0%, 100% { 
                transform: scale(1);
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            50% { 
                transform: scale(1.08);
                box-shadow: 0 15px 40px rgba(69, 183, 209, 0.5);
            }
        }
        
        .avatar-eyes {
            position: absolute;
            top: 30%;
            width: 100%;
            display: flex;
            justify-content: space-around;
            padding: 0 60px;
        }
        
        .eye {
            width: 15px;
            height: 15px;
            background: white;
            border-radius: 50%;
            position: relative;
            animation: blink 4s infinite;
        }
        
        .eye::after {
            content: '';
            position: absolute;
            top: 2px;
            left: 2px;
            width: 8px;
            height: 8px;
            background: #333;
            border-radius: 50%;
            animation: eyeMove 3s infinite;
        }
        
        @keyframes blink {
            0%, 90%, 100% { transform: scaleY(1); }
            95% { transform: scaleY(0.1); }
        }
        
        @keyframes eyeMove {
            0%, 100% { transform: translate(0, 0); }
            25% { transform: translate(2px, -1px); }
            50% { transform: translate(-1px, 1px); }
            75% { transform: translate(1px, -2px); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Edu.ai - Sam Avatar Assistant</h1>
        
        <div class="avatar-display" id="avatar">
            <div class="avatar-face">
                🧑‍🏫
                <div class="avatar-eyes">
                    <div class="eye"></div>
                    <div class="eye"></div>
                </div>
            </div>
        </div>
        
        <div class="status" id="status">
            Ready to start! Click "Start Sam" to begin your AI learning adventure! 🚀<br>
            <small id="setup-check">Checking Azure setup...</small>
        </div>
        
        <div style="text-align: center;">
            <button class="btn" id="startBtn" onclick="startAvatar()">🎤 Start Sam</button>
            <button class="btn" id="stopBtn" onclick="stopAvatar()" disabled style="background: #f44336;">⏹️ Stop Sam</button>
            <a href="/tts-avatar" class="btn" style="background: linear-gradient(45deg, #9C27B0, #E91E63); text-decoration: none; display: inline-block;">🎬 Create Avatar Video</a>
        </div>
        
        <div style="margin-top: 30px; text-align: center;">
            <p><strong>Instructions:</strong></p>
            <ul style="text-align: left; max-width: 500px; margin: 0 auto;">
                <li>Make sure your microphone and speakers are connected</li>
                <li>Click "Start Sam" to begin</li>
                <li>Say "Hello Sam" to start the conversation</li>
                <li>Ask about AI, programming, or anything you want to learn!</li>
                <li>Sam will respond in a fun, kid-friendly way</li>
            </ul>
        </div>
    </div>
    
    <script>
        let isRunning = false;
        
        function updateStatus(message, isError = false) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.style.background = isError ? 'rgba(244, 67, 54, 0.3)' : 'rgba(76, 175, 80, 0.3)';
        }
        
        function updateAvatar(state) {
            const avatar = document.getElementById('avatar');
            const statusEl = document.getElementById('status');
            
            // Remove all state classes
            avatar.classList.remove('speaking', 'listening', 'thinking', 'idle');
            
            switch(state) {
                case 'speaking':
                    avatar.classList.add('speaking');
                    statusEl.textContent = '🗣️ Sam is speaking...';
                    break;
                case 'listening':
                    avatar.classList.add('listening');
                    statusEl.textContent = '👂 Sam is listening to you...';
                    break;
                case 'thinking':
                    avatar.classList.add('thinking');
                    statusEl.textContent = '🤔 Sam is thinking...';
                    break;
                case 'idle':
                default:
                    avatar.classList.add('idle');
                    break;
            }
        }
        
        function simulateConversation() {
            if (!isRunning) return;
            
            // Simulate listening
            updateAvatar('listening');
            setTimeout(() => {
                if (!isRunning) return;
                
                // Simulate thinking
                updateAvatar('thinking');
                setTimeout(() => {
                    if (!isRunning) return;
                    
                    // Simulate speaking
                    updateAvatar('speaking');
                    setTimeout(() => {
                        if (!isRunning) return;
                        updateAvatar('listening');
                        
                        // Schedule next cycle
                        setTimeout(simulateConversation, Math.random() * 10000 + 5000);
                    }, Math.random() * 4000 + 2000);
                }, Math.random() * 2000 + 1000);
            }, Math.random() * 3000 + 2000);
        }
        
        async function startAvatar() {
            const startBtn = document.getElementById('startBtn');
            const stopBtn = document.getElementById('stopBtn');
            
            startBtn.disabled = true;
            updateStatus('🔄 Starting Sam... Please wait!');
            updateAvatar(false);
            
            try {
                const response = await fetch('/start-avatar', {
                    method: 'POST'
                });
                
                const result = await response.json();
                
                if (result.success) {
                    isRunning = true;
                    startBtn.disabled = true;
                    stopBtn.disabled = false;
                    updateStatus('✅ Sam is ready! Say "Hello Sam" to start! 🎉');
                    updateAvatar('listening');
                    
                    // Start conversation simulation
                    setTimeout(simulateConversation, 2000);
                } else {
                    startBtn.disabled = false;
                    updateStatus('❌ Failed to start Sam: ' + result.error, true);
                }
            } catch (error) {
                startBtn.disabled = false;
                updateStatus('❌ Error: ' + error.message, true);
            }
        }
        
        async function stopAvatar() {
            const startBtn = document.getElementById('startBtn');
            const stopBtn = document.getElementById('stopBtn');
            
            try {
                const response = await fetch('/stop-avatar', {
                    method: 'POST'
                });
                
                const result = await response.json();
                
                isRunning = false;
                startBtn.disabled = false;
                stopBtn.disabled = true;
                updateStatus('👋 Sam has stopped. Thanks for learning with me!');
                updateAvatar('idle');
                
            } catch (error) {
                updateStatus('❌ Error stopping Sam: ' + error.message, true);
            }
        }
        
        // Check setup on page load
        window.addEventListener('load', async () => {
            try {
                const response = await fetch('/check-setup');
                const result = await response.json();
                const setupCheck = document.getElementById('setup-check');
                
                if (result.configured) {
                    setupCheck.innerHTML = '✅ Azure setup verified!';
                    setupCheck.style.color = '#4CAF50';
                } else {
                    setupCheck.innerHTML = '❌ ' + result.message;
                    setupCheck.style.color = '#f44336';
                    updateStatus('⚠️ Setup required: ' + result.help, true);
                    
                    // Disable start button if not configured
                    document.getElementById('startBtn').disabled = true;
                    document.getElementById('startBtn').textContent = '⚙️ Setup Required';
                }
            } catch (error) {
                console.log('Setup check failed:', error);
                document.getElementById('setup-check').innerHTML = '⚠️ Unable to check setup';
            }
        });
        
        // Check status periodically
        setInterval(async () => {
            if (isRunning) {
                try {
                    const response = await fetch('/status');
                    const result = await response.json();
                    
                    if (!result.running) {
                        isRunning = false;
                        document.getElementById('startBtn').disabled = false;
                        document.getElementById('stopBtn').disabled = true;
                        updateStatus('👋 Sam has finished. Click "Start Sam" to begin again!');
                        updateAvatar(false);
                    }
                } catch (error) {
                    console.log('Status check error:', error);
                }
            }
        }, 3000);
    </script>
</body>
</html>
    """)

@app.route('/check-setup')
def check_setup():
    """Check if Azure credentials are properly configured"""
    try:
        if not setup_environment():
            return jsonify({
                'configured': False, 
                'message': 'Please configure your Azure OpenAI credentials in .env file',
                'help': 'Copy .env.example to .env and add your Azure keys'
            })
        
        endpoint = os.environ.get('AZURE_VOICELIVE_ENDPOINT', '').strip()
        api_key = os.environ.get('AZURE_VOICELIVE_API_KEY', '').strip()
        
        if not endpoint or not api_key:
            return jsonify({
                'configured': False,
                'message': 'Azure credentials are empty. Please check your .env file',
                'help': 'Make sure AZURE_VOICELIVE_ENDPOINT and AZURE_VOICELIVE_API_KEY are set'
            })
        
        return jsonify({
            'configured': True,
            'message': 'Azure credentials are configured correctly! ✅',
            'endpoint': endpoint[:30] + '...' if len(endpoint) > 30 else endpoint
        })
        
    except Exception as e:
        return jsonify({
            'configured': False,
            'message': f'Error checking setup: {str(e)}',
            'help': 'Please check your .env file configuration'
        })

@app.route('/start-avatar', methods=['POST'])
def start_avatar():
    """Start Avatar process"""
    global avatar_process, avatar_thread
    
    if avatar_process and avatar_process.poll() is None:
        return jsonify({'success': False, 'error': 'Avatar is already running'})
    
    try:
        # Start Avatar in a separate thread
        avatar_thread = threading.Thread(target=run_avatar_process)
        avatar_thread.daemon = True
        avatar_thread.start()
        
        # Give it a moment to start
        time.sleep(2)
        
        return jsonify({'success': True, 'message': 'Avatar started successfully'})
        
    except Exception as e:
        logger.error(f"Error starting Avatar: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/stop-avatar', methods=['POST'])
def stop_avatar():
    """Stop Avatar process"""
    global avatar_process
    
    try:
        if avatar_process and avatar_process.poll() is None:
            avatar_process.terminate()
            avatar_process.wait(timeout=5)
            
        return jsonify({'success': True, 'message': 'Avatar stopped successfully'})
        
    except Exception as e:
        logger.error(f"Error stopping Avatar: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/status')
def get_status():
    """Get Avatar status"""
    global avatar_process
    
    running = avatar_process is not None and avatar_process.poll() is None
    return jsonify({
        'running': running,
        'pid': avatar_process.pid if running else None
    })

def cleanup():
    """Cleanup on exit"""
    global avatar_process
    if avatar_process and avatar_process.poll() is None:
        avatar_process.terminate()

# TTS Avatar Integration
# Store job status globally for tracking
tts_jobs = {}

def _get_tts_headers():
    """Get headers for TTS Avatar API calls"""
    return {
        'Ocp-Apim-Subscription-Key': os.getenv('AZURE_TTS_KEY') or os.getenv('AZURE_SPEECH_KEY'),
        'Content-Type': 'application/json'
    }

@app.route('/tts-avatar')
def tts_avatar_page():
    """Serve TTS Avatar creation page"""
    try:
        with open('tts-avatar.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return jsonify({'error': 'TTS Avatar page not found'}), 404

@app.route('/create-tts-avatar', methods=['POST'])
def create_tts_avatar():
    """Create TTS Avatar video"""
    try:
        data = request.get_json()
        text = data.get('text', 'مرحباً من Edu.ai!')
        character = data.get('character', 'lisa-casual-sitting')
        
        # Get TTS endpoint and key
        endpoint = os.getenv('AZURE_TTS_ENDPOINT') or os.getenv('AZURE_SPEECH_ENDPOINT')
        if not endpoint:
            return jsonify({'success': False, 'error': 'TTS endpoint not configured'})
        
        if not endpoint.endswith('/'):
            endpoint += '/'
        
        # Create unique job ID
        job_id = str(uuid.uuid4())
        
        # Prepare payload
        payload = {
            "synthesisConfig": {
                "voice": "en-US-JennyMultilingualV2Neural",
            },
            "inputKind": "plainText",
            "inputs": [{"content": text}],
            "avatarConfig": {
                "customized": False,
                "talkingAvatarCharacter": character,
                "videoFormat": "mp4",
                "videoCodec": "h264",
                "subtitleType": "soft_embedded",
                "backgroundColor": "#FFFFFFFF",
            }
        }
        
        url = f'{endpoint}avatar/batchsyntheses/{job_id}?api-version=2024-04-15-preview'
        headers = _get_tts_headers()
        
        logger.info(f"Creating TTS Avatar with job ID: {job_id}")
        
        response = requests.put(url, json=payload, headers=headers)
        
        if response.status_code == 201:
            # Store job info
            tts_jobs[job_id] = {
                'status': 'NotStarted',
                'text': text,
                'character': character,
                'created_at': time.time()
            }
            
            logger.info(f"TTS Avatar job created successfully: {job_id}")
            return jsonify({
                'success': True,
                'job_id': job_id,
                'message': 'TTS Avatar job submitted successfully'
            })
        else:
            logger.error(f"Failed to create TTS Avatar: {response.text}")
            return jsonify({
                'success': False,
                'error': f'Failed to submit job: {response.text}'
            })
            
    except Exception as e:
        logger.error(f"Error creating TTS Avatar: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/check-tts-status/<job_id>')
def check_tts_status(job_id):
    """Check TTS Avatar job status"""
    try:
        endpoint = os.getenv('AZURE_TTS_ENDPOINT') or os.getenv('AZURE_SPEECH_ENDPOINT')
        if not endpoint.endswith('/'):
            endpoint += '/'
            
        url = f'{endpoint}avatar/batchsyntheses/{job_id}?api-version=2024-04-15-preview'
        headers = _get_tts_headers()
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            status = result.get('status', 'Unknown')
            
            # Update stored job info
            if job_id in tts_jobs:
                tts_jobs[job_id]['status'] = status
            
            response_data = {'status': status}
            
            if status == 'Succeeded' and 'outputs' in result:
                download_url = result.get('outputs', {}).get('result')
                if download_url:
                    response_data['download_url'] = download_url
                    logger.info(f"TTS Avatar job completed: {job_id}")
            elif status == 'Failed':
                error_info = result.get('properties', {}).get('error', {})
                error_msg = error_info.get('message', 'Unknown error')
                response_data['error'] = error_msg
                logger.error(f"TTS Avatar job failed: {job_id} - {error_msg}")
            
            return jsonify(response_data)
        else:
            return jsonify({
                'status': 'Error',
                'error': f'Failed to check status: {response.text}'
            })
            
    except Exception as e:
        logger.error(f"Error checking TTS status: {str(e)}")
        return jsonify({
            'status': 'Error',
            'error': str(e)
        })

def main():
    """Main function"""
    # Setup signal handlers
    signal.signal(signal.SIGINT, lambda s, f: cleanup())
    signal.signal(signal.SIGTERM, lambda s, f: cleanup())
    
    print("🎓 Starting Edu.ai Avatar Web Server...")
    print("📍 Access the app at: http://localhost:5000")
    print("🤖 Sam is ready to teach AI to kids!")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    finally:
        cleanup()

if __name__ == '__main__':
    main()