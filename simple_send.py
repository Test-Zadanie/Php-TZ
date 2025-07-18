#!/usr/bin/env python3
"""
Simple message sender
"""
import urllib.request
import urllib.parse
import json

BOT_TOKEN = "2143877832:AAGO0ssY0d-d87xrxs3fOOIAno_qg2DVC3k"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, message):
    """Send message to Telegram user"""
    try:
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        req = urllib.request.Request(
            f"{TELEGRAM_API_URL}/sendMessage",
            data=urllib.parse.urlencode(data).encode(),
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            return result.get('ok', False)
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_chat_id():
    """Get chat ID from last message"""
    try:
        with urllib.request.urlopen(f"{TELEGRAM_API_URL}/getUpdates") as response:
            result = json.loads(response.read().decode())
            updates = result.get('result', [])
            
            if updates:
                last_message = updates[-1]
                if 'message' in last_message:
                    chat_id = last_message['message']['chat']['id']
                    user_name = last_message['message']['from']['first_name']
                    return chat_id, user_name
            return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None

# Get user info
chat_id, user_name = get_chat_id()

if chat_id:
    print(f"Sending message to {user_name} (ID: {chat_id})")
    
    # Send response
    message = f"""Welcome to Telegram Notifications Service!

Hello {user_name}! You have been successfully registered.

Your bot is working and ready to send notifications!

Service status: ONLINE
Database: Connected
Notifications: Enabled

You will receive notifications when tasks are sent via API."""
    
    success = send_message(chat_id, message)
    
    if success:
        print("SUCCESS: Message sent to Telegram!")
        print("\nNow test the notification system:")
        print("Send a task via API to see notifications in action.")
    else:
        print("FAILED: Could not send message")
else:
    print("No messages found. Send /start to @TestNewNewTest_bot first.")