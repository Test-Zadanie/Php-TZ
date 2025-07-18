#!/usr/bin/env python3
"""
Send message directly to chat ID
"""
import urllib.request
import urllib.parse
import json
import sys

BOT_TOKEN = "2143877832:AAGO0ssY0d-d87xrxs3fOOIAno_qg2DVC3k"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, message):
    """Send message to specific chat ID"""
    try:
        data = {
            'chat_id': chat_id,
            'text': message
        }
        
        req = urllib.request.Request(
            f"{TELEGRAM_API_URL}/sendMessage",
            data=urllib.parse.urlencode(data).encode(),
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print(f"Response: {result}")
            return result.get('ok', False)
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_bot_info():
    """Get bot information"""
    try:
        with urllib.request.urlopen(f"{TELEGRAM_API_URL}/getMe") as response:
            result = json.loads(response.read().decode())
            if result.get('ok'):
                bot_info = result['result']
                print(f"Bot: {bot_info['first_name']} (@{bot_info['username']})")
                return True
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=== Direct Message Test ===")
    
    # Check bot
    if not get_bot_info():
        print("Bot not accessible")
        sys.exit(1)
    
    # Since we can't get your chat ID directly, let's try a different approach
    print("\nTo get your chat ID:")
    print("1. Send any message to @TestNewNewTest_bot")
    print("2. Go to: https://api.telegram.org/bot2143877832:AAGO0ssY0d-d87xrxs3fOOIAno_qg2DVC3k/getUpdates")
    print("3. Look for 'chat':{'id': YOUR_CHAT_ID}")
    print("4. Use that ID to send direct messages")
    
    # Test with a known chat ID (you'll need to replace this)
    test_chat_id = input("\nEnter your chat ID (or press Enter to skip): ").strip()
    
    if test_chat_id:
        print(f"Sending test message to chat ID: {test_chat_id}")
        
        message = "Hello! This is a test message from your Telegram notification service. The bot is working correctly!"
        
        success = send_message(test_chat_id, message)
        
        if success:
            print("SUCCESS: Message sent!")
        else:
            print("FAILED: Could not send message")
    else:
        print("Skipped direct message test")
    
    print("\nBot is ready to receive messages and send notifications!")