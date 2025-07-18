#!/usr/bin/env python3
"""
Clear webhook and get fresh updates
"""
import urllib.request
import urllib.parse
import json

BOT_TOKEN = "2143877832:AAGO0ssY0d-d87xrxs3fOOIAno_qg2DVC3k"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def clear_webhook():
    """Clear webhook"""
    try:
        data = {'url': ''}
        req = urllib.request.Request(
            f"{TELEGRAM_API_URL}/setWebhook",
            data=urllib.parse.urlencode(data).encode(),
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            return result.get('ok', False)
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_updates():
    """Get updates"""
    try:
        with urllib.request.urlopen(f"{TELEGRAM_API_URL}/getUpdates") as response:
            result = json.loads(response.read().decode())
            return result.get('result', [])
    except Exception as e:
        print(f"Error: {e}")
        return []

print("=== Clearing Webhook ===")

# Clear webhook
success = clear_webhook()
if success:
    print("Webhook cleared successfully")
else:
    print("Failed to clear webhook")

# Get updates
print("\nGetting updates...")
updates = get_updates()
print(f"Found {len(updates)} updates")

for update in updates:
    if 'message' in update:
        msg = update['message']
        chat_id = msg['chat']['id']
        user_name = msg['from']['first_name']
        text = msg.get('text', '')
        
        print(f"Message from {user_name} (ID: {chat_id}): '{text}'")

print("\nWebhook cleared. Now you can:")
print("1. Send a NEW /start message to @TestNewNewTest_bot")
print("2. Run the get_chat_id.py script to see it")
print("3. Bot will respond with welcome message")