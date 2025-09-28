#!/usr/bin/env python
# coding: utf-8

# Simple TTS Avatar test with working character names

import json
import logging
import os
import sys
import time
import uuid
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

# Get credentials
SPEECH_ENDPOINT = os.getenv('AZURE_TTS_ENDPOINT') or os.getenv('AZURE_SPEECH_ENDPOINT')
SUBSCRIPTION_KEY = os.getenv('AZURE_TTS_KEY') or os.getenv('AZURE_SPEECH_KEY')

if not SPEECH_ENDPOINT.endswith('/'):
    SPEECH_ENDPOINT += '/'

API_VERSION = "2024-04-15-preview"

def create_simple_avatar(text):
    """Create TTS Avatar with correct configuration"""
    job_id = str(uuid.uuid4())
    
    # Correct payload structure based on working example
    payload = {
        "synthesisConfig": {
            "voice": "en-US-JennyMultilingualV2Neural"
        },
        "inputKind": "plainText", 
        "inputs": [{"content": text}],
        "avatarConfig": {
            "customized": False,
            "talkingAvatarCharacter": "Lisa",  # Use proper character name
            "talkingAvatarStyle": "casual-sitting",  # Required style
            "videoFormat": "mp4",
            "videoCodec": "h264",
            "subtitleType": "soft_embedded",
            "backgroundColor": "#FFFFFFFF"
        }
    }
    
    url = f'{SPEECH_ENDPOINT}avatar/batchsyntheses/{job_id}?api-version={API_VERSION}'
    headers = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
        'Content-Type': 'application/json'
    }
    
    logger.info(f"🚀 Creating Avatar with minimal config...")
    logger.info(f"📊 Text length: {len(text)} characters, {len(text.split())} words")
    logger.info(f"⏱️ Estimated duration: ~{len(text.split()) / 150 * 60:.1f} seconds")
    
    start_time = time.time()
    
    try:
        # Submit job
        response = requests.put(url, json=payload, headers=headers)
        
        if response.status_code == 201:
            logger.info(f"✅ Job submitted: {job_id}")
            
            # Poll for completion
            max_attempts = 36
            for attempt in range(max_attempts):
                time.sleep(10)
                
                check_response = requests.get(url, headers=headers)
                if check_response.status_code == 200:
                    result = check_response.json()
                    status = result.get('status')
                    elapsed = time.time() - start_time
                    
                    logger.info(f"📊 Status: {status} (elapsed: {elapsed:.0f}s)")
                    
                    if status == 'Succeeded':
                        download_url = result.get('outputs', {}).get('result', 'No URL')
                        logger.info(f"🎉 SUCCESS! Total time: {elapsed:.1f} seconds")
                        logger.info(f"🔗 Download: {download_url}")
                        return True
                        
                    elif status == 'Failed':
                        error = result.get('properties', {}).get('error', {})
                        logger.error(f"❌ Failed: {error.get('message', 'Unknown error')}")
                        logger.error(f"Full error: {json.dumps(error, indent=2)}")
                        return False
                        
            logger.error(f"⏰ Timeout after {time.time() - start_time:.1f} seconds")
            return False
            
        else:
            logger.error(f"❌ Submit failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Exception: {e}")
        return False

if __name__ == '__main__':
    text = """Hello, my friends! My name is Loly, and today I will teach you something special from Microsoft Learn. We will talk about one type of Artificial Intelligence called Computer Vision.

Computer Vision helps computers see and understand pictures. Just like your eyes help you know if you see a dog or a cat, AI can look at a picture and say, 'This is a cat!' or 'This is a car!'

For example, when you use your phone camera and it puts a square on your face, that is Computer Vision at work. It is like giving the computer little eyes so it can understand the world.

So, Computer Vision is one way AI helps us every day. Great job learning with me today!"""
    
    logger.info("🎓 COMPUTER VISION AVATAR TEST")
    logger.info("=" * 50)
    
    if create_simple_avatar(text):
        logger.info("=" * 50)
        logger.info("✅ Avatar created successfully!")
    else:
        logger.error("=" * 50) 
        logger.error("❌ Avatar creation failed!")