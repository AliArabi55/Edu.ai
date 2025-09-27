#!/usr/bin/env python3
"""
Enhanced Avatar.py with Visual Sync
Connects the visual avatar with the voice conversation
"""

import asyncio
import threading
import time
import json
from pathlib import Path
import websockets
import logging

# Import the original Avatar functionality
import sys
import os

# Add the path to import the original Avatar
sys.path.append(str(Path(__file__).parent))

# Import original Avatar components
try:
    from Avatar import AudioProcessor, BasicVoiceAssistant, parse_arguments
    from Avatar import AzureKeyCredential, InteractiveBrowserCredential
    from Avatar import logger as avatar_logger
except ImportError as e:
    print(f"Could not import Avatar components: {e}")
    print("Make sure Avatar.py is in the same directory")
    sys.exit(1)

logger = logging.getLogger(__name__)

class VisualAvatarController:
    """Controls the visual avatar state based on voice conversation"""
    
    def __init__(self):
        self.websocket_clients = set()
        self.current_state = "idle"
        self.is_speaking = False
        self.is_listening = False
        
    async def register_websocket(self, websocket):
        """Register a new websocket client"""
        self.websocket_clients.add(websocket)
        # Send current state to new client
        await self.send_state_update()
        
    async def unregister_websocket(self, websocket):
        """Unregister a websocket client"""
        self.websocket_clients.discard(websocket)
        
    async def set_state(self, state):
        """Update avatar state and notify all clients"""
        if self.current_state != state:
            self.current_state = state
            await self.send_state_update()
            
    async def send_state_update(self):
        """Send state update to all connected clients"""
        if self.websocket_clients:
            message = json.dumps({
                'type': 'avatar_state',
                'state': self.current_state,
                'timestamp': time.time()
            })
            
            # Send to all connected clients
            disconnected = set()
            for websocket in self.websocket_clients:
                try:
                    await websocket.send(message)
                except websockets.exceptions.ConnectionClosed:
                    disconnected.add(websocket)
                    
            # Remove disconnected clients
            for websocket in disconnected:
                self.websocket_clients.discard(websocket)
                
    async def start_listening(self):
        """Avatar started listening"""
        await self.set_state("listening")
        
    async def start_thinking(self):
        """Avatar is processing/thinking"""
        await self.set_state("thinking")
        
    async def start_speaking(self):
        """Avatar started speaking"""
        await self.set_state("speaking")
        
    async def stop_activity(self):
        """Avatar returned to idle state"""
        await self.set_state("idle")

# Global avatar controller
avatar_controller = VisualAvatarController()

class EnhancedVoiceAssistant(BasicVoiceAssistant):
    """Enhanced voice assistant with visual avatar sync"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.avatar_controller = avatar_controller
        
    async def handle_server_event(self, event):
        """Handle server events and update visual avatar"""
        event_type = event.get("type")
        
        if event_type == "session.created":
            await self.avatar_controller.set_state("listening")
        elif event_type == "input_audio_buffer.speech_started":
            await self.avatar_controller.start_listening()
        elif event_type == "input_audio_buffer.speech_stopped":
            await self.avatar_controller.start_thinking()
        elif event_type == "response.audio.started":
            await self.avatar_controller.start_speaking()
        elif event_type == "response.audio.done":
            await self.avatar_controller.start_listening()
        elif event_type == "error":
            await self.avatar_controller.stop_activity()
            
        # Call parent handler if it exists
        if hasattr(super(), 'handle_server_event'):
            await super().handle_server_event(event)

async def websocket_handler(websocket, path):
    """Handle websocket connections from the web interface"""
    await avatar_controller.register_websocket(websocket)
    try:
        async for message in websocket:
            # Handle incoming messages if needed
            try:
                data = json.loads(message)
                if data.get('type') == 'ping':
                    await websocket.send(json.dumps({'type': 'pong'}))
            except json.JSONDecodeError:
                pass
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        await avatar_controller.unregister_websocket(websocket)

def start_websocket_server():
    """Start the websocket server for avatar synchronization"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    start_server = websockets.serve(websocket_handler, "localhost", 8765)
    loop.run_until_complete(start_server)
    logger.info("Avatar WebSocket server started on ws://localhost:8765")
    loop.run_forever()

async def main():
    """Main function with enhanced avatar"""
    
    # Start WebSocket server in background thread
    websocket_thread = threading.Thread(target=start_websocket_server, daemon=True)
    websocket_thread.start()
    
    # Import and run the enhanced assistant
    args = parse_arguments()
    
    # Validate credentials
    if not args.api_key and not args.use_token_credential:
        print("❌ Error: No authentication provided")
        return 1

    try:
        # Create client with appropriate credential
        if args.use_token_credential:
            credential = InteractiveBrowserCredential()
            logger.info("Using Azure token credential")
        else:
            credential = AzureKeyCredential(args.api_key)
            logger.info("Using API key credential")

        # Create and start enhanced voice assistant
        assistant = EnhancedVoiceAssistant(
            endpoint=args.endpoint,
            credential=credential,
            model=args.model,
            voice=args.voice,
            instructions=args.instructions,
        )

        # Start the assistant
        await assistant.start()

    except KeyboardInterrupt:
        print("\n👋 Enhanced Avatar assistant shut down. Goodbye!")
        await avatar_controller.stop_activity()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Error: {e}")
        await avatar_controller.stop_activity()
        return 1

def parse_arguments():
    """Parse command line arguments for Enhanced Avatar."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Enhanced Avatar Voice Assistant with Visual Sync",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--api-key",
        help="Azure VoiceLive API key. If not provided, will use AZURE_VOICELIVE_API_KEY environment variable.",
        type=str,
        default=os.environ.get("AZURE_VOICELIVE_API_KEY"),
    )

    parser.add_argument(
        "--endpoint",
        help="Azure VoiceLive endpoint",
        type=str,
        default=os.environ.get("AZURE_VOICELIVE_ENDPOINT", "wss://api.voicelive.com/v1"),
    )

    parser.add_argument(
        "--model",
        help="VoiceLive model to use",
        type=str,
        default=os.environ.get("VOICELIVE_MODEL", "gpt-4o-realtime-preview"),
    )

    parser.add_argument(
        "--voice",
        help="Voice to use for the assistant",
        type=str,
        default=os.environ.get("VOICELIVE_VOICE", "en-US-AvaNeural"),
        choices=[
            "alloy",
            "echo",
            "fable",
            "onyx",
            "nova",
            "shimmer",
            "en-US-AvaNeural",
            "en-US-JennyNeural",
            "en-US-GuyNeural",
        ],
    )

    parser.add_argument(
        "--instructions",
        help="System instructions for the AI assistant",
        type=str,
        default=os.environ.get(
            "VOICELIVE_INSTRUCTIONS",
            "Act as 'Sam,' a friendly English teacher who explains Artificial Intelligence (AI) to children (ages 6–18) in a very simple, fun, and easy way. Keep responses short (under four sentences) and full of clarity. Use playful and friendly tone with warmth, using emojis and cheerful expressions. Use super simple English, small words, and short sentences that even a 6-year-old can understand. Always praise the child's ideas and answers to build curiosity and confidence. Begin with bright, exciting greetings like 'Hello, my friend! I am Sam!' Ask playful questions to connect AI with their world. Use fun, short stories and encourage them to guess. Give instant, positive feedback like 'Yes, great idea! You are so smart! 🌟' End sessions with energy and excitement for next time.",
        ),
    )

    parser.add_argument(
        "--use-token-credential", help="Use Azure token credential instead of API key", action="store_true"
    )

    parser.add_argument("--verbose", help="Enable verbose logging", action="store_true")

    return parser.parse_args()

if __name__ == "__main__":
    print("🚀 Enhanced Avatar with Visual Sync")
    print("🔗 WebSocket server: ws://localhost:8765")
    print("🎤 Voice Assistant: Azure VoiceLive SDK")
    print("=" * 50)
    
    asyncio.run(main())