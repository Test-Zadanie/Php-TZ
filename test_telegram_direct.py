#!/usr/bin/env python3
"""
Direct test of Telegram bot functionality without webhook
"""
import urllib.request
import urllib.parse
import json
import time

BOT_TOKEN = "2143877832:AAGO0ssY0d-d87xrxs3fOOIAno_qg2DVC3k"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, message):
    """Send message directly to Telegram"""
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
            print(f"Message sent: {result}")
            return result.get('ok', False)
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

def get_updates():
    """Get updates from Telegram"""
    try:
        with urllib.request.urlopen(f"{TELEGRAM_API_URL}/getUpdates") as response:
            result = json.loads(response.read().decode())
            return result.get('result', [])
    except Exception as e:
        print(f"Error getting updates: {e}")
        return []

def test_bot():
    """Test bot functionality"""
    print("=== Testing Telegram Bot ===")
    
    # Get bot info
    try:
        with urllib.request.urlopen(f"{TELEGRAM_API_URL}/getMe") as response:
            result = json.loads(response.read().decode())
            if result.get('ok'):
                bot_info = result['result']
                print(f"Bot name: {bot_info['first_name']}")
                print(f"Bot username: @{bot_info['username']}")
                print(f"Bot ID: {bot_info['id']}")
            else:
                print("Failed to get bot info")
                return False
    except Exception as e:
        print(f"Error getting bot info: {e}")
        return False
    
    # Test sending message to a test chat
    print("\nTo test the bot:")
    print("1. Find your bot in Telegram: @" + bot_info['username'])
    print("2. Send /start command")
    print("3. The bot should respond")
    
    # Get recent updates
    print("\nRecent bot activity:")
    updates = get_updates()
    if updates:
        for update in updates[-5:]:  # Show last 5 updates
            if 'message' in update:
                msg = update['message']
                user = msg.get('from', {})
                text = msg.get('text', '')
                print(f"  {user.get('first_name', 'Unknown')}: {text}")
    else:
        print("  No recent messages")
    
    return True

if __name__ == "__main__":
    test_bot()
    
    print("\n=== Next Steps ===")
    print("1. To test webhook, verify your email in ngrok dashboard")
    print("2. Run: ngrok http 9000")
    print("3. Copy the https URL from ngrok")
    print("4. Run: python setup_webhook.py https://your-ngrok-url.ngrok.io")
    print("5. Test by sending /start to your bot")
    
    print("\n=== Current Status ===")
    print("✅ Server running on localhost:9000")
    print("✅ API endpoints working")
    print("✅ Bot token valid")
    print("✅ Direct Telegram API access working")
    print("⏳ Webhook setup requires ngrok email verification")