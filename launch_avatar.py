#!/usr/bin/env python3
"""
Avatar Launcher Script for Edu.ai
This script launches the Avatar.py with proper environment variables and error handling.
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_environment():
    """Setup environment variables for Avatar.py"""
    # Get the project root directory
    project_root = Path(__file__).parent
    env_file = project_root / '.env'
    
    if env_file.exists():
        print(f"📁 Loading environment from: {env_file}")
        # Load environment variables manually
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print("✅ Environment variables loaded")
    else:
        print("⚠️  .env file not found")
    
    # Print loaded environment variables (masked)
    print("\n🔐 Environment Configuration:")
    for key in ['AZURE_VOICELIVE_ENDPOINT', 'AZURE_VOICELIVE_API_KEY', 'AZURE_VOICELIVE_REGION']:
        value = os.environ.get(key, 'Not Set')
        if 'KEY' in key and value != 'Not Set':
            masked_value = value[:8] + '...' + value[-8:]
            print(f"   {key}: {masked_value}")
        else:
            print(f"   {key}: {value}")

def run_avatar():
    """Run the Avatar.py script"""
    avatar_script = Path(__file__).parent / 'Edu.ai' / '6.2' / 'Avatar.py'
    
    if not avatar_script.exists():
        print(f"❌ Avatar.py not found at: {avatar_script}")
        return False
    
    print(f"\n🚀 Starting Avatar from: {avatar_script}")
    
    try:
        # Run Avatar.py with proper arguments
        cmd = [
            sys.executable, 
            str(avatar_script),
            '--endpoint', os.environ.get('AZURE_VOICELIVE_ENDPOINT', ''),
            '--api-key', os.environ.get('AZURE_VOICELIVE_API_KEY', ''),
            '--model', 'gpt-4o-realtime-preview',
            '--voice', 'alloy',
            '--instructions', 'You are a helpful AI tutor for Edu.ai platform. Help students learn coding and AI concepts in an engaging way.'
        ]
        
        print(f"💻 Running command: {' '.join(cmd[:6])} [HIDDEN_KEY] {' '.join(cmd[8:])}")
        
        # Run the Avatar script
        result = subprocess.run(cmd, 
                              capture_output=False,
                              text=True,
                              cwd=str(avatar_script.parent))
        
        if result.returncode == 0:
            print("✅ Avatar completed successfully")
            return True
        else:
            print(f"❌ Avatar exited with code: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error running Avatar: {e}")
        return False

def main():
    """Main function"""
    print("🤖 Edu.ai Avatar Launcher")
    print("=" * 40)
    
    # Setup environment
    setup_environment()
    
    # Check if required environment variables are set
    required_vars = ['AZURE_VOICELIVE_ENDPOINT', 'AZURE_VOICELIVE_API_KEY']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        print("Please check your .env file")
        return 1
    
    # Run Avatar
    if run_avatar():
        print("\n👋 Avatar session completed!")
        return 0
    else:
        print("\n❌ Avatar session failed!")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)