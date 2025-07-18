#!/usr/bin/env python3
"""
Get all updates and respond
"""
import urllib.request
import urllib.parse
import json

BOT_TOKEN = "2143877832:AAGO0ssY0d-d87xrxs3fOOIAno_qg2DVC3k"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_all_updates():
    """Get all updates"""
    try:
        url = f"{TELEGRAM_API_URL}/getUpdates"
        with urllib.request.urlopen(url) as response:
            result = json.loads(response.read().decode())
            return result.get('result', [])
    except Exception as e:
        print(f"Error: {e}")
        return []

def send_message(chat_id, message):
    """Send message"""
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
            return result.get('ok', False)
    except Exception as e:
        print(f"Error: {e}")
        return False

# Get all updates
updates = get_all_updates()
print(f"Found {len(updates)} updates")

for update in updates:
    if 'message' in update:
        msg = update['message']
        chat_id = msg['chat']['id']
        text = msg.get('text', '')
        user_name = msg['from']['first_name']
        
        print(f"Message from {user_name}: '{text}' (Chat ID: {chat_id})")
        
        if text == '/start':
            print(f"Responding to {user_name}...")
            
            response = f"Hello {user_name}! Welcome to the Telegram Notifications Service. You are now registered and will receive notifications!"
            
            success = send_message(chat_id, response)
            
            if success:
                print("Response sent successfully!")
            else:
                print("Failed to send response")

print("\nDone processing updates")