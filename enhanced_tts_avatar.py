#!/usr/bin/env python
# coding: utf-8
"""
Enhanced TTS Avatar Generator for Edu.ai
Creates AI-powered avatar videos with custom text and voices
"""

import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
import requests

# Load environment variables
load_dotenv()

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
        format="[%(asctime)s] %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")
logger = logging.getLogger(__name__)

# Configuration
SPEECH_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT', "https://gpt4oali-8-june-gradutu-resource.cognitiveservices.azure.com/")
PASSWORDLESS_AUTHENTICATION = False
API_VERSION = "2024-04-15-preview"

# Available Voices and Avatars
AVAILABLE_VOICES = {
    'jenny': 'en-US-JennyMultilingualNeural',
    'aria': 'en-US-AriaNeural', 
    'guy': 'en-US-GuyNeural',
    'davis': 'en-US-DavisNeural'
}

AVAILABLE_AVATARS = {
    'lisa': {'character': 'Lisa', 'style': 'casual-sitting'},
    'anna': {'character': 'Anna', 'style': 'graceful-sitting'},
    'joy': {'character': 'Joy', 'style': 'casual-standing'},
}

def _create_job_id():
    """Create a unique job ID"""
    return uuid.uuid4()

def _authenticate():
    """Authenticate with Azure"""
    if PASSWORDLESS_AUTHENTICATION:
        credential = DefaultAzureCredential()
        token = credential.get_token('https://cognitiveservices.azure.com/.default')
        return {'Authorization': f'Bearer {token.token}'}
    else:
        SUBSCRIPTION_KEY = os.getenv("AZURE_OPENAI_KEY")
        if not SUBSCRIPTION_KEY:
            logger.error("AZURE_OPENAI_KEY not found in environment variables!")
            sys.exit(1)
        return {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY}

def create_avatar_video(text, voice='jenny', avatar='lisa', output_name=None):
    """
    Create an avatar video with specified text, voice, and avatar
    
    Args:
        text (str): Text to be spoken
        voice (str): Voice to use (jenny, aria, guy, davis)
        avatar (str): Avatar to use (lisa, anna, joy)
        output_name (str): Optional name for output file
    
    Returns:
        str: Download URL of the generated video
    """
    
    job_id = _create_job_id()
    
    # Get voice and avatar settings
    voice_name = AVAILABLE_VOICES.get(voice, AVAILABLE_VOICES['jenny'])
    avatar_config = AVAILABLE_AVATARS.get(avatar, AVAILABLE_AVATARS['lisa'])
    
    logger.info(f"Creating avatar video...")
    logger.info(f"Voice: {voice} ({voice_name})")
    logger.info(f"Avatar: {avatar} ({avatar_config['character']} - {avatar_config['style']})")
    logger.info(f"Text: {text}")
    
    url = f'{SPEECH_ENDPOINT}/avatar/batchsyntheses/{job_id}?api-version={API_VERSION}'
    header = {
        'Content-Type': 'application/json'
    }
    header.update(_authenticate())
    
    payload = {
        'synthesisConfig': {
            "voice": voice_name
        },
        'customVoices': {},
        "inputKind": "plainText",
        "inputs": [
            {
                "content": text,
            },
        ],
        "avatarConfig": {
            "customized": False,
            "talkingAvatarCharacter": avatar_config['character'],
            "talkingAvatarStyle": avatar_config['style'],
            "videoFormat": "mp4",
            "videoCodec": "h264",
            "subtitleType": "soft_embedded",
            "backgroundColor": "#FFFFFFFF",
        }
    }
    
    # Submit job
    response = requests.put(url, json.dumps(payload), headers=header)
    if response.status_code >= 400:
        logger.error(f'Failed to submit batch avatar synthesis job: [{response.status_code}], {response.text}')
        return None
    
    logger.info('Batch avatar synthesis job submitted successfully')
    logger.info(f'Job ID: {response.json()["id"]}')
    
    # Wait for completion
    while True:
        status_response = requests.get(url, headers=_authenticate())
        if status_response.status_code >= 400:
            logger.error(f'Failed to get batch synthesis job: {status_response.text}')
            return None
            
        status_data = status_response.json()
        status = status_data['status']
        
        if status == 'Succeeded':
            download_url = status_data["outputs"]["result"]
            logger.info(f'✅ Avatar video created successfully!')
            logger.info(f'📹 Download URL: {download_url}')
            
            # Download the video if output name is provided
            if output_name:
                download_video(download_url, output_name)
            
            return download_url
            
        elif status == 'Failed':
            logger.error('❌ Avatar synthesis job failed')
            return None
            
        else:
            logger.info(f'🔄 Processing... Status: {status}')
            time.sleep(5)

def download_video(url, filename):
    """Download video from URL"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            logger.info(f'✅ Video downloaded: {filename}')
            return True
        else:
            logger.error(f'Failed to download video: {response.status_code}')
            return False
    except Exception as e:
        logger.error(f'Error downloading video: {e}')
        return False

def create_sam_introduction():
    """Create Sam's introduction video"""
    intro_text = """
    Hi there! I'm Sam, your friendly AI teacher from Edu.ai! 
    I'm so excited to help you learn about artificial intelligence in a fun and easy way. 
    Whether you're 6 years old or 18, I'll explain everything using simple words and exciting examples.
    We'll explore how AI works, how it helps people, and maybe even build some cool projects together!
    Are you ready to start this amazing learning adventure with me? Let's go!
    """
    
    return create_avatar_video(
        text=intro_text.strip(),
        voice='jenny',
        avatar='lisa',
        output_name=f'sam_intro_{datetime.now().strftime("%Y%m%d_%H%M%S")}.mp4'
    )

def create_custom_lesson(topic, level='beginner'):
    """Create a custom lesson video"""
    
    lessons = {
        'ai_basics': {
            'beginner': "Let's talk about Artificial Intelligence! AI is like giving a computer a brain so it can think and learn, just like you do! Imagine if your computer could recognize your voice, understand what you're saying, and even talk back to you. That's AI in action!",
            'intermediate': "Artificial Intelligence is a field of computer science that enables machines to perform tasks that typically require human intelligence. This includes learning from data, recognizing patterns, making decisions, and solving problems.",
            'advanced': "AI encompasses machine learning algorithms, neural networks, and deep learning architectures that can process vast amounts of data to identify complex patterns and make predictions or decisions with minimal human intervention."
        },
        'machine_learning': {
            'beginner': "Machine Learning is like teaching a computer to learn from examples! Just like how you learn to recognize different animals by seeing lots of pictures, computers can learn too by looking at lots of data and finding patterns.",
            'intermediate': "Machine Learning is a subset of AI where algorithms learn from data to make predictions or decisions without being explicitly programmed for every specific task.",
            'advanced': "Machine Learning employs statistical techniques and algorithms like regression, classification, clustering, and reinforcement learning to enable systems to automatically improve their performance on specific tasks through experience."
        }
    }
    
    if topic in lessons and level in lessons[topic]:
        lesson_text = f"Welcome to today's lesson about {topic.replace('_', ' ').title()}! {lessons[topic][level]}"
        
        return create_avatar_video(
            text=lesson_text,
            voice='jenny',
            avatar='lisa',
            output_name=f'lesson_{topic}_{level}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.mp4'
        )
    else:
        logger.error(f"Lesson not found: {topic} ({level})")
        return None

def main():
    """Main function for interactive avatar creation"""
    print("\n🎓 Welcome to Edu.ai TTS Avatar Generator!")
    print("=" * 50)
    
    while True:
        print("\nWhat would you like to create?")
        print("1. Sam's Introduction Video")
        print("2. Custom AI Lesson")
        print("3. Custom Text Video")
        print("4. List Available Voices & Avatars")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            print("\n🎬 Creating Sam's Introduction Video...")
            create_sam_introduction()
            
        elif choice == '2':
            print("\nAvailable Topics:")
            print("- ai_basics")
            print("- machine_learning")
            topic = input("Enter topic: ").strip()
            
            print("\nLevels: beginner, intermediate, advanced")
            level = input("Enter level (default: beginner): ").strip() or 'beginner'
            
            print(f"\n🎬 Creating lesson: {topic} ({level})...")
            create_custom_lesson(topic, level)
            
        elif choice == '3':
            text = input("\nEnter your text: ").strip()
            if not text:
                print("❌ Text cannot be empty!")
                continue
                
            print(f"\nVoices: {', '.join(AVAILABLE_VOICES.keys())}")
            voice = input("Choose voice (default: jenny): ").strip() or 'jenny'
            
            print(f"\nAvatars: {', '.join(AVAILABLE_AVATARS.keys())}")
            avatar = input("Choose avatar (default: lisa): ").strip() or 'lisa'
            
            filename = input("Output filename (optional): ").strip() or None
            
            print(f"\n🎬 Creating custom video...")
            create_avatar_video(text, voice, avatar, filename)
            
        elif choice == '4':
            print("\n🎤 Available Voices:")
            for key, value in AVAILABLE_VOICES.items():
                print(f"  {key}: {value}")
                
            print("\n👤 Available Avatars:")
            for key, value in AVAILABLE_AVATARS.items():
                print(f"  {key}: {value['character']} ({value['style']})")
                
        elif choice == '5':
            print("\n👋 Goodbye! Happy learning with Edu.ai!")
            break
            
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == '__main__':
    main()