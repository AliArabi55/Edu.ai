@echo off
title Edu.ai - Complete Application Launcher
color 0a

echo.
echo ===============================================
echo   🎓 Edu.ai - Complete Application Launcher
echo ===============================================
echo.

cd /d "C:\Users\aliar\OneDrive\Documents\GitHub\Edu.ai"

echo 🔧 Setting up environment...

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo ❌ IMPORTANT: .env file not found!
    echo.
    echo You need to create a .env file with your Azure credentials.
    echo Here's how to set it up:
    echo.
    echo 1. Copy the example file:
    echo    copy .env.example .env
    echo.
    echo 2. Edit the .env file and add your Azure OpenAI credentials
    echo    notepad .env
    echo.
    echo 3. Save the file and run this launcher again
    echo.
    echo ⚠️  The Avatar (Sam) won't work without proper Azure setup!
    echo    But you can still explore the main website.
    echo.
    echo Press any key to continue anyway (Avatar will be disabled)
    pause
    echo.
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python first.
    pause
    exit /b 1
)

echo ✅ Python is available

REM Install required packages if not already installed
echo 📦 Installing required packages...
python -m pip install Flask azure-ai-voicelive pyaudio python-dotenv >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Some packages might not install correctly, but continuing...
) else (
    echo ✅ All packages are ready
)

echo.
echo 🚀 Starting Edu.ai services...
echo.

REM Start the main HTTP server in background
echo 🌐 Starting main website server (Port 8000)...
start "Edu.ai Main Server" /min cmd /c "python -m http.server 8000 & echo Main server started on http://localhost:8000 & pause"

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Start the Avatar server in background
echo 🤖 Starting Sam Avatar server (Port 5000)...
start "Sam Avatar Server" /min cmd /c "python avatar_server.py & echo Avatar server started on http://localhost:5000 & pause"

REM Wait a moment
timeout /t 3 /nobreak >nul

echo.
echo ✅ All servers are starting up!
echo.
echo 📱 Access the application:
echo    Main Website: http://localhost:8000
echo    Sam Avatar:   http://localhost:5000
echo.
echo 🎯 Quick Start Guide:
echo    1. Open http://localhost:8000 in your browser
echo    2. Navigate through the learning path
echo    3. When you reach "Start Avatar Lesson", click it
echo    4. Sam will be ready to teach you about AI!
echo.
echo 💡 Tips:
echo    - Make sure your microphone and speakers are connected
echo    - Sam speaks English and is great with kids ages 6-18
echo    - Say "Hello Sam" to start the conversation
echo.

REM Open the main application in default browser
echo 🌍 Opening main application in your browser...
timeout /t 2 /nobreak >nul
start http://localhost:8000

echo.
echo 🎉 Edu.ai is ready! Enjoy learning with Sam!
echo.
echo Press any key to close this launcher window...
pause >nul