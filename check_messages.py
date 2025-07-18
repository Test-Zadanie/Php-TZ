#!/usr/bin/env python3
"""
Check for new messages from Telegram
"""
import urllib.request
import json

BOT_TOKEN = "2143877832:AAGO0ssY0d-d87xrxs3fOOIAno_qg2DVC3k"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def check_messages():
    """Check for new messages"""
    try:
        with urllib.request.urlopen(f"{TELEGRAM_API_URL}/getUpdates") as response:
            result = json.loads(response.read().decode())
            updates = result.get('result', [])
            
            print(f"Total updates: {len(updates)}")
            
            for update in updates[-5:]:  # Show last 5 messages
                if 'message' in update:
                    msg = update['message']
                    user = msg.get('from', {})
                    text = msg.get('text', '')
                    date = msg.get('date', 0)
                    
                    user_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
                    
                    print(f"Message from {user_name}: '{text}' (Update ID: {update['update_id']})")
            
            return updates
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    print("=== Checking Telegram Messages ===")
    messages = check_messages()
    
    if messages:
        print(f"\nFound {len(messages)} total messages")
        print("The polling bot should have processed them.")
    else:
        print("\nNo messages found")
    
    print("\nTo test:")
    print("1. Send /start to @TestNewNewTest_bot")
    print("2. Bot should respond immediately")
    print("3. Check this script again to see new messages")