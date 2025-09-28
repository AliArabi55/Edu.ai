#!/usr/bin/env python
# coding: utf-8

# Timer Test for TTS Avatar Creation - Accurate Timing

import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime
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

def create_timed_avatar(text, character="Lisa", style="casual-sitting"):
    """Create TTS Avatar with precise timing measurements"""
    
    # Start timing
    total_start = time.time()
    start_time = datetime.now()
    
    logger.info("=" * 60)
    logger.info(f"🎬 STARTING TTS AVATAR CREATION")
    logger.info(f"⏰ Start Time: {start_time.strftime('%H:%M:%S.%f')[:-3]}")
    logger.info("=" * 60)
    
    job_id = str(uuid.uuid4())
    
    # Analyze text
    word_count = len(text.split())
    char_count = len(text)
    estimated_duration = (word_count / 150) * 60 + 3  # words per minute + buffer
    
    logger.info(f"📊 TEXT ANALYSIS:")
    logger.info(f"   📝 Characters: {char_count}")
    logger.info(f"   📝 Words: {word_count}")
    logger.info(f"   ⏱️ Estimated video duration: {estimated_duration:.1f} seconds")
    logger.info(f"   🎯 Expected processing time: 30-90 seconds")
    
    # Payload
    payload = {
        "synthesisConfig": {
            "voice": "en-US-JennyMultilingualV2Neural"
        },
        "inputKind": "plainText", 
        "inputs": [{"content": text}],
        "avatarConfig": {
            "customized": False,
            "talkingAvatarCharacter": character,
            "talkingAvatarStyle": style,
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
    
    # Submit job timing
    submit_start = time.time()
    logger.info(f"🚀 SUBMITTING JOB...")
    logger.info(f"   🆔 Job ID: {job_id}")
    logger.info(f"   👤 Character: {character} ({style})")
    
    try:
        response = requests.put(url, json=payload, headers=headers)
        submit_end = time.time()
        submit_time = submit_end - submit_start
        
        logger.info(f"⚡ Submit completed in: {submit_time:.2f} seconds")
        
        if response.status_code == 201:
            logger.info("✅ Job submitted successfully")
            
            # Processing phase timing
            processing_start = time.time()
            logger.info(f"⏳ PROCESSING PHASE STARTED...")
            
            max_attempts = 40  # 6+ minutes max
            attempt = 0
            
            for attempt in range(max_attempts):
                check_start = time.time()
                
                time.sleep(8)  # Check every 8 seconds
                
                check_response = requests.get(url, headers=headers)
                check_end = time.time()
                check_time = check_end - check_start
                
                if check_response.status_code == 200:
                    result = check_response.json()
                    status = result.get('status')
                    
                    processing_elapsed = time.time() - processing_start
                    total_elapsed = time.time() - total_start
                    
                    logger.info(f"📊 Status Check #{attempt + 1}:")
                    logger.info(f"   📈 Status: {status}")
                    logger.info(f"   ⏱️ Processing time: {processing_elapsed:.1f}s")
                    logger.info(f"   ⏱️ Total time: {total_elapsed:.1f}s")
                    logger.info(f"   🔗 Check took: {check_time:.2f}s")
                    
                    if status == 'Succeeded':
                        final_time = time.time()
                        total_duration = final_time - total_start
                        processing_duration = final_time - processing_start
                        end_time = datetime.now()
                        
                        download_url = result.get('outputs', {}).get('result', 'No URL')
                        
                        logger.info("=" * 60)
                        logger.info("🎉 AVATAR CREATION COMPLETED SUCCESSFULLY!")
                        logger.info("=" * 60)
                        logger.info(f"⏰ End Time: {end_time.strftime('%H:%M:%S.%f')[:-3]}")
                        logger.info(f"⏱️ TIMING BREAKDOWN:")
                        logger.info(f"   📤 Submit phase: {submit_time:.2f} seconds")
                        logger.info(f"   ⚙️ Processing phase: {processing_duration:.2f} seconds")
                        logger.info(f"   🎯 Total duration: {total_duration:.2f} seconds")
                        logger.info(f"   📊 Attempts: {attempt + 1}")
                        logger.info(f"   📈 Efficiency: {word_count / total_duration:.2f} words/second")
                        logger.info("=" * 60)
                        logger.info(f"🔗 Download URL: {download_url}")
                        
                        return {
                            'success': True,
                            'total_time': total_duration,
                            'processing_time': processing_duration,
                            'submit_time': submit_time,
                            'attempts': attempt + 1,
                            'words_per_second': word_count / total_duration,
                            'download_url': download_url,
                            'word_count': word_count,
                            'char_count': char_count
                        }
                        
                    elif status == 'Failed':
                        error = result.get('properties', {}).get('error', {})
                        logger.error("=" * 60)
                        logger.error("❌ AVATAR CREATION FAILED!")
                        logger.error(f"   ❌ Error: {error.get('message', 'Unknown error')}")
                        logger.error(f"   ⏱️ Failed after: {time.time() - total_start:.2f} seconds")
                        logger.error("=" * 60)
                        return {'success': False, 'error': error.get('message', 'Unknown error')}
                else:
                    logger.error(f"❌ Status check failed: {check_response.status_code}")
                    
            logger.error(f"⏰ Timeout after {time.time() - total_start:.2f} seconds")
            return {'success': False, 'error': 'Timeout'}
            
        else:
            logger.error(f"❌ Submit failed: {response.status_code} - {response.text}")
            return {'success': False, 'error': f'Submit failed: {response.status_code}'}
            
    except Exception as e:
        logger.error(f"❌ Exception: {e}")
        return {'success': False, 'error': str(e)}

if __name__ == '__main__':
    # New test text about Machine Learning
    test_text = """Hi everyone! I'm Lisa, your AI teacher. Today we'll explore Machine Learning - another amazing type of Artificial Intelligence!

Machine Learning is like teaching a computer to learn from examples, just like how you learn to recognize animals by seeing many pictures of cats and dogs.

Imagine showing a computer thousands of photos labeled 'cat' and 'dog'. After studying all these examples, the computer learns to identify cats and dogs in new photos it has never seen before!

This is exactly how Netflix recommends movies you might like, or how your email knows which messages are spam. The computer learned patterns from millions of examples.

Machine Learning is helping us solve problems in medicine, transportation, and education. It's everywhere around us, making our lives easier and smarter every day!"""
    
    logger.info("🧠 Testing with Machine Learning topic")
    logger.info("=" * 60)
    
    result = create_timed_avatar(test_text, "Lisa", "casual-sitting")
    
    if result['success']:
        logger.info("🎊 FINAL SUMMARY:")
        logger.info(f"✅ Total Time: {result['total_time']:.2f} seconds")
        logger.info(f"⚙️ Processing: {result['processing_time']:.2f} seconds") 
        logger.info(f"📊 Efficiency: {result['words_per_second']:.2f} words/sec")
        logger.info(f"📝 Content: {result['word_count']} words, {result['char_count']} chars")
    else:
        logger.error(f"❌ Creation failed: {result['error']}")