#!/usr/bin/env python
# coding: utf-8

# Test TTS Avatar with custom text about Computer Vision

import json
import logging
import os
import sys
import time
import uuid
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
        format="[%(asctime)s] %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")
logger = logging.getLogger(__name__)

# Get credentials from environment variables (SECURE)
SPEECH_ENDPOINT = os.getenv('AZURE_TTS_ENDPOINT') or os.getenv('AZURE_SPEECH_ENDPOINT')
SUBSCRIPTION_KEY = os.getenv('AZURE_TTS_KEY') or os.getenv('AZURE_SPEECH_KEY')
SPEECH_REGION = os.getenv('AZURE_TTS_REGION') or os.getenv('AZURE_SPEECH_REGION')

# Validate required environment variables
if not SPEECH_ENDPOINT:
    logger.error("❌ AZURE_TTS_ENDPOINT or AZURE_SPEECH_ENDPOINT not found in .env file!")
    sys.exit(1)
    
if not SUBSCRIPTION_KEY:
    logger.error("❌ AZURE_TTS_KEY or AZURE_SPEECH_KEY not found in .env file!")
    sys.exit(1)

# Clean endpoint URL
if not SPEECH_ENDPOINT.endswith('/'):
    SPEECH_ENDPOINT += '/'

logger.info(f"✅ Using endpoint: {SPEECH_ENDPOINT}")
logger.info(f"✅ Using region: {SPEECH_REGION}")

API_VERSION = "2024-04-15-preview"

def _create_job_id():
    """Create a unique job ID"""
    return str(uuid.uuid4())

def _get_headers():
    """Get authentication headers"""
    return {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
        'Content-Type': 'application/json'
    }

def calculate_video_duration(text):
    """Calculate approximate video duration based on text length"""
    # Average speaking rate: ~150 words per minute
    # Adding buffer time for avatar animations
    words = len(text.split())
    base_duration = (words / 150) * 60  # seconds
    buffer_time = 3  # seconds for intro/outro animations
    total_duration = base_duration + buffer_time
    return max(total_duration, 5)  # minimum 5 seconds

def submit_synthesis(job_id, text, character="lisa"):
    """Submit TTS Avatar synthesis job"""
    url = f'{SPEECH_ENDPOINT}avatar/batchsyntheses/{job_id}?api-version={API_VERSION}'
    
    # Calculate estimated duration
    estimated_duration = calculate_video_duration(text)
    word_count = len(text.split())
    
    logger.info(f"📊 TEXT ANALYSIS:")
    logger.info(f"   📝 Word count: {word_count} words")
    logger.info(f"   ⏱️ Estimated video duration: {estimated_duration:.1f} seconds")
    logger.info(f"   🎬 Processing time estimate: 30-90 seconds")
    
    # Use supported character names
    supported_characters = {
        "lisa": "lisa",
        "anna": "anna", 
        "sara": "sara"
    }
    
    avatar_character = supported_characters.get(character.lower(), "lisa")
    
    # Improved payload
    payload = {
        "synthesisConfig": {
            "voice": "en-US-JennyMultilingualV2Neural",  # Good for educational content
        },
        "inputKind": "plainText",
        "inputs": [
            {
                "content": text,
            },
        ],
        "avatarConfig": {
            "customized": False,
            "talkingAvatarCharacter": avatar_character,
            "videoFormat": "mp4",
            "videoCodec": "h264",
            "subtitleType": "soft_embedded",
            "backgroundColor": "#FFFFFFFF",
        }
    }
    
    headers = _get_headers()
    
    logger.info(f"🚀 Submitting TTS Avatar job with ID: {job_id}")
    logger.info(f"👤 Character: {avatar_character} (requested: {character})")
    
    try:
        start_time = time.time()
        response = requests.put(url, json=payload, headers=headers)
        submit_time = time.time() - start_time
        
        logger.info(f"⚡ Submit request took: {submit_time:.2f} seconds")
        
        if response.status_code == 201:
            logger.info('✅ Batch avatar synthesis job submitted successfully')
            logger.info(f'🆔 Job ID: {job_id}')
            return True
        else:
            logger.error(f'❌ Failed to submit batch avatar synthesis job')
            logger.error(f'Status Code: {response.status_code}')
            logger.error(f'Response: {response.text}')
            return False
            
    except Exception as e:
        logger.error(f'❌ Exception occurred: {str(e)}')
        return False

def get_synthesis(job_id):
    """Get synthesis job status with detailed information"""
    url = f'{SPEECH_ENDPOINT}avatar/batchsyntheses/{job_id}?api-version={API_VERSION}'
    headers = _get_headers()
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            status = result.get('status', 'Unknown')
            
            # If completed successfully, show download URL
            if status == 'Succeeded' and 'outputs' in result:
                if 'result' in result['outputs']:
                    download_url = result['outputs']['result']
                    logger.info(f"🎉 SUCCESS! Video ready for download:")
                    logger.info(f"🔗 Download URL: {download_url}")
            
            # If failed, show error details
            elif status == 'Failed':
                if 'properties' in result and 'error' in result['properties']:
                    error_info = result['properties']['error']
                    logger.error(f"❌ Error Code: {error_info.get('code', 'Unknown')}")
                    logger.error(f"❌ Error Message: {error_info.get('message', 'No details')}")
                
                logger.error(f"❌ Full response: {json.dumps(result, indent=2)}")
            
            return status
        else:
            logger.error(f'❌ Failed to get batch synthesis job: {response.text}')
            return None
            
    except Exception as e:
        logger.error(f'❌ Exception occurred while checking status: {str(e)}')
        return None

def create_tts_avatar_with_timing(text, character="lisa"):
    """Main function to create TTS Avatar with detailed timing"""
    
    logger.info("🎬 Starting TTS Avatar creation process...")
    logger.info(f"📝 Input text preview: {text[:100]}...")
    
    job_id = _create_job_id()
    overall_start_time = time.time()
    
    if submit_synthesis(job_id, text, character):
        logger.info("⏳ Waiting for synthesis to complete...")
        
        processing_start_time = time.time()
        max_attempts = 36  # Maximum 6 minutes (36 * 10 seconds)
        attempt = 0
        
        while attempt < max_attempts:
            status = get_synthesis(job_id)
            
            current_time = time.time()
            processing_time = current_time - processing_start_time
            total_time = current_time - overall_start_time
            
            if status == 'Succeeded':
                logger.info('🎉 Batch avatar synthesis job succeeded!')
                logger.info(f"⏱️ TIMING SUMMARY:")
                logger.info(f"   📊 Processing time: {processing_time:.1f} seconds")
                logger.info(f"   🎯 Total time: {total_time:.1f} seconds")
                return True
            elif status == 'Failed':
                logger.error('❌ Batch avatar synthesis job failed!')
                logger.error(f"⏱️ Failed after {total_time:.1f} seconds")
                return False
            elif status in ['NotStarted', 'Running']:
                logger.info(f'⏳ Processing... {processing_time:.0f}s elapsed (attempt {attempt + 1}/{max_attempts})')
                time.sleep(10)  # Wait 10 seconds
            else:
                logger.warning(f'⚠️ Unknown status: {status}')
                time.sleep(10)
            
            attempt += 1
        
        logger.error(f"⏰ Timeout after {total_time:.1f} seconds")
        return False
    else:
        logger.error("❌ Failed to submit TTS Avatar job")
        return False

if __name__ == '__main__':
    # Your custom text about Computer Vision
    computer_vision_text = """Hello, my friends! My name is Loly, and today I will teach you something special from Microsoft Learn. We will talk about one type of Artificial Intelligence called Computer Vision.

Computer Vision helps computers see and understand pictures. Just like your eyes help you know if you see a dog or a cat, AI can look at a picture and say, 'This is a cat!' or 'This is a car!'

For example, when you use your phone camera and it puts a square on your face, that is Computer Vision at work. It is like giving the computer little eyes so it can understand the world.

So, Computer Vision is one way AI helps us every day. Great job learning with me today!"""
    
    logger.info("🎓 Creating Educational TTS Avatar about Computer Vision")
    logger.info("=" * 60)
    
    success = create_tts_avatar_with_timing(computer_vision_text, "lisa")
    
    if success:
        logger.info("=" * 60)
        logger.info("✅ TTS Avatar created successfully! Check the download link above.")
    else:
        logger.error("=" * 60)
        logger.error("❌ TTS Avatar creation failed!")