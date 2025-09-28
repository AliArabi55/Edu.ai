
#!/usr/bin/env python
# coding: utf-8

# Edu.ai TTS Avatar Integration
# Uses secure environment variables for Azure credentials

import json
import logging
import os
import sys
import time
import uuid
from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
import requests

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(stream=sys.stdout, level=logging.INFO,  # set to logging.DEBUG for verbose output
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

logger.info(f"✅ Using endpoint: {SPEECH_ENDPOINT}")
logger.info(f"✅ Using region: {SPEECH_REGION}")

# Use key-based authentication for simplicity
PASSWORDLESS_AUTHENTICATION = False
API_VERSION = "2024-04-15-preview"

def _create_job_id():
    # the job ID must be unique in current speech resource
    # you can use a GUID or a self-increasing number
    return uuid.uuid4()

def _authenticate():
    if PASSWORDLESS_AUTHENTICATION:
        # Use Azure Identity for passwordless authentication
        credential = DefaultAzureCredential()
        token = credential.get_token('https://cognitiveservices.azure.com/.default')
        return {'Authorization': f'Bearer {token.token}'}
    else:
        # Use subscription key from environment variables (SECURE)
        return {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY}

def submit_synthesis(job_id: str):
    url = f'{SPEECH_ENDPOINT}/avatar/batchsyntheses/{job_id}?api-version={API_VERSION}'
    header = {
        'Content-Type': 'application/json'
    }
    header.update(_authenticate())
    isCustomized = False

    payload = {
        'synthesisConfig': {
            # "voice": 'en-US-JennyMultilingualNeural'
            "voice": '{VOICE_NAME}', 
        },
        # Replace with your custom voice name and deployment ID if you want to use custom voice.
        # Multiple voices are supported, the mixture of custom voices and platform voices is allowed.
        # Invalid voice name or deployment ID will be rejected.
        'customVoices': {
            # "YOUR_CUSTOM_VOICE_NAME": "YOUR_CUSTOM_VOICE_ID"
        },
        "inputKind": "plainText",
        "inputs": [
            {
                "content": "Hi, I'm a virtual assistant created by Microsoft.",
            },
        ],
        "avatarConfig":
        {
            "customized": isCustomized, # set to True if you want to use customized avatar
            # "talkingAvatarCharacter": 'Lisa-casual-sitting'
            "talkingAvatarCharacter": '{TALKING_AVATAR_CHARACTER_NAME}',  # talking avatar character
            "videoFormat": "mp4",  # mp4 or webm, webm is required for transparent background
            "videoCodec": "h264",  # hevc, h264 or vp9, vp9 is required for transparent background; default is hevc
            "subtitleType": "soft_embedded",
            "backgroundColor": "#FFFFFFFF", # background color in RGBA format, default is white; can be set to 'transparent' for transparent background
            # "backgroundImage": "https://samples-files.com/samples/Images/jpg/1920-1080-sample.jpg", # background image URL, only support https, either backgroundImage or backgroundColor can be set
        }
        if isCustomized
        else
        {
            "customized": isCustomized, # set to True if you want to use customized avatar
            # "talkingAvatarCharacter": 'Lisa'
            "talkingAvatarCharacter": '{TALKING_AVATAR_CHARACTER}',  # talking avatar character
            # "talkingAvatarStyle": 'casual-sitting'
            "talkingAvatarStyle": '{TALKING_AVATAR_STYLE}',  # talking avatar style, required for prebuilt avatar, optional for custom avatar
            "videoFormat": "mp4",  # mp4 or webm, webm is required for transparent background
            "videoCodec": "h264",  # hevc, h264 or vp9, vp9 is required for transparent background; default is hevc
            "subtitleType": "soft_embedded",
            "backgroundColor": "#FFFFFFFF", # background color in RGBA format, default is white; can be set to 'transparent' for transparent background
            # "backgroundImage": "https://samples-files.com/samples/Images/jpg/1920-1080-sample.jpg", # background image URL, only support https, either backgroundImage or backgroundColor can be set
        }
    }

    response = requests.put(url, json.dumps(payload), headers=header)
    if response.status_code < 400:
        logger.info('Batch avatar synthesis job submitted successfully')
        logger.info(f'Job ID: {response.json()["id"]}')
        return True
    else:
        logger.error(f'Failed to submit batch avatar synthesis job: [{response.status_code}], {response.text}')

def get_synthesis(job_id):
    url = f'{SPEECH_ENDPOINT}/avatar/batchsyntheses/{job_id}?api-version={API_VERSION}'
    header = _authenticate()

    response = requests.get(url, headers=header)
    if response.status_code < 400:
        logger.debug('Get batch synthesis job successfully')
        logger.debug(response.json())
        if response.json()['status'] == 'Succeeded':
            logger.info(f'Batch synthesis job succeeded, download URL: {response.json()["outputs"]["result"]}')
        return response.json()['status']
    else:
        logger.error(f'Failed to get batch synthesis job: {response.text}')

def list_synthesis_jobs(skip: int = 0, max_page_size: int = 100):
    """List all batch synthesis jobs in the subscription"""
    url = f'{SPEECH_ENDPOINT}/avatar/batchsyntheses?api-version={API_VERSION}&skip={skip}&maxpagesize={max_page_size}'
    header = _authenticate()

    response = requests.get(url, headers=header)
    if response.status_code < 400:
        logger.info(f'List batch synthesis jobs successfully, got {len(response.json()["values"])} jobs')
        logger.info(response.json())
    else:
        logger.error(f'Failed to list batch synthesis jobs: {response.text}')

def create_tts_avatar(text=None, character="lisa-casual-sitting"):
    """Main function to create TTS Avatar with enhanced error handling"""
    if not text:
        text = "مرحباً! أنا سام، مدرس اللغة الإنجليزية الذكي. مرحباً بك في Edu.ai!"
    
    job_id = _create_job_id()
    
    logger.info("🎬 Starting TTS Avatar creation process...")
    
    if submit_synthesis(job_id, text, character):
        logger.info("⏳ Waiting for synthesis to complete...")
        
        max_attempts = 20  # Maximum attempts
        attempt = 0
        
        while attempt < max_attempts:
            status = get_synthesis(job_id)
            
            if status == 'Succeeded':
                logger.info('🎉 Batch avatar synthesis job succeeded!')
                return True
            elif status == 'Failed':
                logger.error('❌ Batch avatar synthesis job failed!')
                return False
            elif status in ['NotStarted', 'Running']:
                logger.info(f'⏳ Job processing... (attempt {attempt + 1}/{max_attempts})')
                time.sleep(10)
            else:
                logger.warning(f'⚠️ Unknown status: {status}')
                time.sleep(10)
            
            attempt += 1
        
        logger.error("⏰ Timeout: Job took too long")
        return False
    else:
        logger.error("❌ Failed to submit job")
        return False

if __name__ == '__main__':
    # Test the TTS Avatar
    success = create_tts_avatar()
    if success:
        logger.info("✅ TTS Avatar created successfully!")
    else:
        logger.error("❌ TTS Avatar creation failed!")
            