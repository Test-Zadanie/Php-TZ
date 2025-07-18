#!/usr/bin/env python3
"""
Get chat ID from Telegram API
"""
import urllib.request
import json

BOT_TOKEN = "2143877832:AAGO0ssY0d-d87xrxs3fOOIAno_qg2DVC3k"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_updates():
    """Get updates from Telegram API"""
    try:
        with urllib.request.urlopen(f"{TELEGRAM_API_URL}/getUpdates") as response:
            result = json.loads(response.read().decode())
            return result.get('result', [])
    except Exception as e:
        print(f"Error: {e}")
        return []

def send_message_to_chat(chat_id, message):
    """Send message to specific chat"""
    try:
        import urllib.parse
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
        print(f"Error sending message: {e}")
        return False

print("=== Getting Chat ID ===")
print("Checking for messages...")

updates = get_updates()
print(f"Found {len(updates)} updates")

unique_chats = {}

for update in updates:
    if 'message' in update:
        msg = update['message']
        chat_id = msg['chat']['id']
        user_name = msg['from']['first_name']
        text = msg.get('text', '')
        
        unique_chats[chat_id] = user_name
        
        print(f"Chat ID: {chat_id}, User: {user_name}, Message: '{text}'")

print(f"\nUnique chats found: {len(unique_chats)}")

for chat_id, user_name in unique_chats.items():
    print(f"Chat ID: {chat_id} - {user_name}")
    
    # Send welcome message
    welcome_msg = f"Hello {user_name}! Your Telegram notification service is now active and ready to send notifications!"
    
    success = send_message_to_chat(chat_id, welcome_msg)
    
    if success:
        print(f"  SUCCESS: Welcome message sent to {user_name}")
    else:
        print(f"  FAILED: Could not send message to {user_name}")

if not unique_chats:
    print("\nNo messages found. To test:")
    print("1. Send /start to @TestNewNewTest_bot")
    print("2. Run this script again")
    print("3. Bot will respond with welcome message")

print("\nBot is ready for notifications!")