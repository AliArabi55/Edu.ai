# 🎓 Edu.ai Setup Guide

Welcome to Edu.ai! This guide will help you set up Sam, your AI English teacher.

## 📋 Prerequisites

1. **Python 3.7 or higher** - Download from [python.org](https://python.org)
2. **Azure OpenAI Access** - You need an Azure account with OpenAI service enabled
3. **Microphone and Speakers** - For voice interaction with Sam

## 🚀 Quick Setup

### Step 1: Get Your Azure Credentials

1. Go to [Azure Portal](https://portal.azure.com)
2. Create or access your Azure OpenAI resource
3. Go to "Keys and Endpoint" section
4. Copy your:
   - **API Key** (Key 1 or Key 2)
   - **Endpoint** (looks like: https://your-resource.openai.azure.com/)

### Step 2: Configure Environment

1. Copy the example environment file:
   ```
   copy .env.example .env
   ```

2. Edit the `.env` file with your credentials:
   ```
   notepad .env
   ```

3. Replace the placeholder values:
   ```
   AZURE_OPENAI_API_KEY=your_actual_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   ```

4. Save the file

### Step 3: Start the Application

1. Double-click `start-eduai.bat`
2. The launcher will:
   - Check your setup
   - Install required packages
   - Start both servers
   - Open your browser automatically

## 🌟 Using Sam

1. **Navigate the Learning Path**: Start at `http://localhost:8000`
2. **Meet Sam**: Click through to "Start Lesson" 
3. **Voice Interaction**: 
   - Make sure your mic/speakers are working
   - Say "Hello Sam" to start
   - Ask about AI, programming, or anything!

## 🔧 Troubleshooting

### Avatar Won't Start
- Check your `.env` file has correct Azure credentials
- Ensure your Azure OpenAI service is active
- Visit `http://localhost:5000` to see detailed error messages

### No Sound
- Check Windows sound settings
- Ensure microphone permissions are granted
- Test with Windows Voice Recorder first

### Python Errors
- Make sure Python 3.7+ is installed
- Run `pip install --upgrade pip` first
- Some packages require Visual Studio Build Tools on Windows

## 🎯 Features

- **🧑‍🏫 Sam**: Friendly AI teacher specialized for kids ages 6-18
- **🎤 Voice Chat**: Real-time voice conversation with AI
- **📚 Learning Path**: Structured lessons from basics to advanced
- **🎨 Visual Interface**: Animated avatar with engaging UI
- **🔒 Secure**: Your API keys stay on your computer

## 🆘 Need Help?

If you run into issues:

1. Check the console messages in the launcher
2. Visit `http://localhost:5000/check-setup` for diagnostic info
3. Ensure your Azure subscription has sufficient credits
4. Try running `python avatar_server.py` manually to see detailed errors

## 📝 Important Notes

- **Never commit your `.env` file** - It contains your private API keys!
- **Azure costs money** - Monitor your usage in Azure Portal
- **Internet required** - Sam needs to connect to Azure OpenAI
- **Windows only** - This setup is optimized for Windows systems

Enjoy learning with Sam! 🚀✨