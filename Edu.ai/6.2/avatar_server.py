#!/usr/bin/env python3
"""
Enhanced Avatar Server with WebSocket Sync
Real-time visual avatar synchronized with voice conversation
"""

from flask import Flask, render_template_string, jsonify, request
import subprocess
import threading
import time
import logging
import os
import signal
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variables
avatar_process = None
avatar_thread = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sam - مساعدك التعليمي الذكي</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
        }

        .container {
            text-align: center;
            max-width: 800px;
            padding: 20px;
        }

        .avatar-container {
            position: relative;
            width: 300px;
            height: 300px;
            margin: 0 auto 30px;
            border-radius: 50%;
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4, #FECA57);
            background-size: 300% 300%;
            animation: gradientShift 8s ease infinite;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .avatar-face {
            width: 280px;
            height: 280px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 50%;
            position: relative;
            animation: breathe 4s ease-in-out infinite;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        @keyframes breathe {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        .avatar-eyes {
            position: absolute;
            top: 35%;
            width: 100%;
            display: flex;
            justify-content: space-around;
            padding: 0 60px;
        }

        .eye {
            width: 30px;
            height: 30px;
            background: #333;
            border-radius: 50%;
            position: relative;
            animation: blink 6s infinite;
        }

        @keyframes blink {
            0%, 90%, 100% { transform: scaleY(1); }
            95% { transform: scaleY(0.1); }
        }

        .avatar-mouth {
            position: absolute;
            bottom: 35%;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 30px;
            border: 3px solid #333;
            border-top: none;
            border-radius: 0 0 60px 60px;
            transition: all 0.3s ease;
        }

        /* Avatar States */
        .speaking .avatar-container {
            animation: gradientShift 2s ease infinite, borderGlow 1s ease-in-out infinite;
        }

        .speaking .avatar-mouth {
            animation: speak 0.5s ease-in-out infinite alternate;
        }

        @keyframes speak {
            0% { transform: translateX(-50%) scaleY(1); }
            100% { transform: translateX(-50%) scaleY(1.3); }
        }

        .listening .avatar-container {
            animation: gradientShift 4s ease infinite, pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        .listening .eye {
            animation: blink 6s infinite, listen 2s ease-in-out infinite;
        }

        @keyframes listen {
            0%, 100% { transform: scaleX(1); }
            50% { transform: scaleX(1.2); }
        }

        .thinking .avatar-container {
            animation: gradientShift 6s ease infinite;
            opacity: 0.8;
        }

        .thinking .eye {
            animation: blink 1s infinite, lookAround 3s infinite;
        }

        @keyframes lookAround {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }

        .idle .avatar-container {
            animation: gradientShift 8s ease infinite;
        }

        .idle .eye {
            animation: blink 6s infinite;
        }

        @keyframes borderGlow {
            0%, 100% { box-shadow: 0 20px 60px rgba(0,0,0,0.3), 0 0 30px rgba(255,255,255,0.3); }
            50% { box-shadow: 0 20px 60px rgba(0,0,0,0.3), 0 0 50px rgba(255,255,255,0.8); }
        }

        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 30px;
        }

        .status {
            background: rgba(255,255,255,0.2);
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 1.1em;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }

        .controls {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }

        .btn {
            padding: 12px 25px;
            border: none;
            border-radius: 25px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s ease;
            background: rgba(255,255,255,0.2);
            color: white;
            backdrop-filter: blur(10px);
        }

        .btn:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }

        .btn.primary {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        }

        .btn.primary:hover {
            background: linear-gradient(45deg, #FF5252, #26D0CE);
        }

        .info-panel {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            margin-top: 30px;
            backdrop-filter: blur(10px);
            text-align: right;
        }

        .loading {
            display: none;
            margin: 20px 0;
        }

        .loading.show {
            display: block;
        }

        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s ease-in-out infinite;
            margin: 0 auto;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .connection-status {
            position: absolute;
            top: 20px;
            right: 20px;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            backdrop-filter: blur(10px);
        }

        .connection-status.connected {
            background: rgba(76, 175, 80, 0.3);
            border: 1px solid rgba(76, 175, 80, 0.5);
        }

        .connection-status.disconnected {
            background: rgba(244, 67, 54, 0.3);
            border: 1px solid rgba(244, 67, 54, 0.5);
        }

        .connection-status.connecting {
            background: rgba(255, 193, 7, 0.3);
            border: 1px solid rgba(255, 193, 7, 0.5);
        }
    </style>
</head>
<body>
    <div class="connection-status" id="connectionStatus">جاري الاتصال...</div>
    
    <div class="container">
        <h1>🤖 Sam</h1>
        <p class="subtitle">مساعدك التعليمي الذكي</p>
        
        <div class="avatar-wrapper" id="avatarWrapper">
            <div class="avatar-container">
                <div class="avatar-face">
                    <div class="avatar-eyes">
                        <div class="eye"></div>
                        <div class="eye"></div>
                    </div>
                    <div class="avatar-mouth"></div>
                </div>
            </div>
        </div>
        
        <div class="status" id="statusText">جاهز للمحادثة</div>
        
        <div class="loading" id="loadingIndicator">
            <div class="spinner"></div>
            <p>جاري تشغيل Sam...</p>
        </div>
        
        <div class="controls">
            <button class="btn primary" onclick="startAvatar()" id="startBtn">🎤 ابدأ المحادثة</button>
            <button class="btn" onclick="stopAvatar()" id="stopBtn">⏹️ إيقاف</button>
            <button class="btn" onclick="testAnimation()" id="testBtn">🧪 اختبار الحركة</button>
        </div>
        
        <div class="info-panel">
            <h3>معلومات هامة:</h3>
            <ul style="text-align: right; list-style: none; padding: 0;">
                <li>🎯 Sam مُصمم لتعليم الأطفال من 6-18 سنة</li>
                <li>🗣️ يستخدم تقنية الذكاء الاصطناعي للمحادثة الصوتية</li>
                <li>🎨 الأفاتار يتفاعل مع حالة المحادثة</li>
                <li>🔊 تأكد من تشغيل السماعات والميكروفون</li>
            </ul>
        </div>
    </div>

    <script>
        let websocket = null;
        let isConnected = false;
        let currentState = 'idle';
        let animationTimer = null;
        
        // WebSocket connection
        function connectWebSocket() {
            try {
                websocket = new WebSocket('ws://localhost:8765');
                
                websocket.onopen = function() {
                    console.log('WebSocket متصل');
                    isConnected = true;
                    updateConnectionStatus('connected', 'متصل بـ Sam');
                };
                
                websocket.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    if (data.type === 'avatar_state') {
                        updateAvatarState(data.state);
                    }
                };
                
                websocket.onclose = function() {
                    console.log('WebSocket منقطع');
                    isConnected = false;
                    updateConnectionStatus('disconnected', 'منقطع');
                    // محاولة إعادة الاتصال
                    setTimeout(connectWebSocket, 3000);
                };
                
                websocket.onerror = function(error) {
                    console.error('خطأ WebSocket:', error);
                    updateConnectionStatus('disconnected', 'خطأ في الاتصال');
                };
                
            } catch (error) {
                console.error('فشل في إنشاء WebSocket:', error);
                updateConnectionStatus('disconnected', 'فشل الاتصال');
            }
        }
        
        function updateConnectionStatus(status, text) {
            const statusEl = document.getElementById('connectionStatus');
            statusEl.className = `connection-status ${status}`;
            statusEl.textContent = text;
        }
        
        function updateAvatarState(state) {
            if (currentState === state) return;
            
            currentState = state;
            const wrapper = document.getElementById('avatarWrapper');
            const statusText = document.getElementById('statusText');
            
            // إزالة جميع الحالات
            wrapper.className = 'avatar-wrapper';
            
            // إضافة الحالة الجديدة
            wrapper.classList.add(state);
            
            // تحديث النص
            switch(state) {
                case 'listening':
                    statusText.textContent = '👂 يستمع إليك...';
                    statusText.style.background = 'rgba(76, 175, 80, 0.3)';
                    break;
                case 'thinking':
                    statusText.textContent = '🧠 يفكر في الإجابة...';
                    statusText.style.background = 'rgba(255, 193, 7, 0.3)';
                    break;
                case 'speaking':
                    statusText.textContent = '🗣️ يتحدث معك...';
                    statusText.style.background = 'rgba(33, 150, 243, 0.3)';
                    break;
                default:
                    statusText.textContent = '😊 جاهز للمحادثة';
                    statusText.style.background = 'rgba(255,255,255,0.2)';
            }
            
            console.log(`تم تغيير حالة الأفاتار إلى: ${state}`);
        }
        
        function startAvatar() {
            const loadingEl = document.getElementById('loadingIndicator');
            const startBtn = document.getElementById('startBtn');
            const statusText = document.getElementById('statusText');
            
            startBtn.disabled = true;
            loadingEl.classList.add('show');
            statusText.textContent = '🚀 جاري تشغيل Sam...';
            
            fetch('/start_avatar', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                console.log('استجابة تشغيل الأفاتار:', data);
                setTimeout(() => {
                    loadingEl.classList.remove('show');
                    startBtn.disabled = false;
                    if (data.status === 'started') {
                        statusText.textContent = '✅ Sam جاهز للمحادثة!';
                        statusText.style.background = 'rgba(76, 175, 80, 0.3)';
                        updateAvatarState('listening');
                    } else {
                        statusText.textContent = '❌ فشل في تشغيل Sam';
                        statusText.style.background = 'rgba(244, 67, 54, 0.3)';
                    }
                }, 2000);
            })
            .catch(error => {
                console.error('خطأ في تشغيل الأفاتار:', error);
                loadingEl.classList.remove('show');
                startBtn.disabled = false;
                statusText.textContent = '❌ خطأ في الاتصال';
                statusText.style.background = 'rgba(244, 67, 54, 0.3)';
            });
        }
        
        function stopAvatar() {
            fetch('/stop_avatar', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                console.log('استجابة إيقاف الأفاتار:', data);
                updateAvatarState('idle');
                document.getElementById('statusText').textContent = '⏹️ تم إيقاف Sam';
            })
            .catch(error => {
                console.error('خطأ في إيقاف الأفاتار:', error);
            });
        }
        
        function testAnimation() {
            const states = ['listening', 'thinking', 'speaking', 'idle'];
            let currentIndex = 0;
            
            if (animationTimer) {
                clearInterval(animationTimer);
            }
            
            document.getElementById('statusText').textContent = '🧪 اختبار الحركات...';
            
            animationTimer = setInterval(() => {
                updateAvatarState(states[currentIndex]);
                currentIndex = (currentIndex + 1) % states.length;
                
                if (currentIndex === 0) {
                    setTimeout(() => {
                        clearInterval(animationTimer);
                        updateAvatarState('idle');
                        document.getElementById('statusText').textContent = '✅ اكتمل اختبار الحركات';
                    }, 2000);
                }
            }, 2000);
        }
        
        // بدء الاتصال عند تحميل الصفحة
        document.addEventListener('DOMContentLoaded', function() {
            updateConnectionStatus('connecting', 'جاري الاتصال...');
            connectWebSocket();
        });
        
        // إرسال ping دوري للحفاظ على الاتصال
        setInterval(() => {
            if (websocket && websocket.readyState === WebSocket.OPEN) {
                websocket.send(JSON.stringify({type: 'ping'}));
            }
        }, 30000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main avatar interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/start_avatar', methods=['POST'])
def start_avatar():
    """Start the enhanced avatar with WebSocket sync"""
    global avatar_process
    
    try:
        if avatar_process is None or avatar_process.poll() is not None:
            # Start the enhanced avatar
            avatar_dir = Path(__file__).parent
            avatar_script = avatar_dir / "Enhanced_Avatar.py"
            
            if not avatar_script.exists():
                logger.error(f"Enhanced Avatar script not found: {avatar_script}")
                return jsonify({
                    'status': 'error',
                    'message': 'Enhanced Avatar script not found'
                })
            
            # Start the process
            avatar_process = subprocess.Popen([
                sys.executable, str(avatar_script)
            ], cwd=str(avatar_dir))
            
            logger.info(f"Started Enhanced Avatar process: PID {avatar_process.pid}")
            
            return jsonify({
                'status': 'started',
                'message': 'Enhanced Avatar started successfully',
                'pid': avatar_process.pid
            })
        else:
            return jsonify({
                'status': 'already_running',
                'message': 'Avatar is already running',
                'pid': avatar_process.pid
            })
    
    except Exception as e:
        logger.error(f"Error starting Enhanced Avatar: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to start Avatar: {str(e)}'
        })

@app.route('/stop_avatar', methods=['POST'])
def stop_avatar():
    """Stop the avatar process"""
    global avatar_process
    
    try:
        if avatar_process and avatar_process.poll() is None:
            avatar_process.terminate()
            avatar_process.wait(timeout=5)
            logger.info("Enhanced Avatar process stopped")
            return jsonify({
                'status': 'stopped',
                'message': 'Avatar stopped successfully'
            })
        else:
            return jsonify({
                'status': 'not_running',
                'message': 'Avatar was not running'
            })
    
    except Exception as e:
        logger.error(f"Error stopping Avatar: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to stop Avatar: {str(e)}'
        })

@app.route('/status')
def status():
    """Get current avatar status"""
    global avatar_process
    
    if avatar_process and avatar_process.poll() is None:
        return jsonify({
            'status': 'running',
            'pid': avatar_process.pid
        })
    else:
        return jsonify({
            'status': 'stopped'
        })

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    global avatar_process
    
    logger.info("Shutting down Avatar Server...")
    
    if avatar_process and avatar_process.poll() is None:
        logger.info("Terminating Enhanced Avatar process...")
        avatar_process.terminate()
        try:
            avatar_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            logger.warning("Force killing Enhanced Avatar process...")
            avatar_process.kill()
    
    sys.exit(0)

if __name__ == '__main__':
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🚀 Starting Enhanced Avatar Server...")
    print("🌐 Visual interface: http://localhost:5000")
    print("🔗 WebSocket sync: ws://localhost:8765")
    print("Press Ctrl+C to stop")
    
    # Start Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )