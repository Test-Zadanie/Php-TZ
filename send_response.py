#!/usr/bin/env python3
"""
Send response to Telegram user
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
            print(f"Message sent: {result}")
            return result.get('ok', False)
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

def get_user_chat_id():
    """Get chat ID from recent messages"""
    try:
        with urllib.request.urlopen(f"{TELEGRAM_API_URL}/getUpdates") as response:
            result = json.loads(response.read().decode())
            updates = result.get('result', [])
            
            if updates:
                last_message = updates[-1]
                if 'message' in last_message:
                    return last_message['message']['chat']['id']
            return None
    except Exception as e:
        print(f"Error getting chat ID: {e}")
        return None

def main():
    print("=== Sending Response to Telegram User ===")
    
    # Get chat ID from recent messages
    chat_id = get_user_chat_id()
    
    if chat_id:
        print(f"Found chat ID: {chat_id}")
        
        # Send welcome message
        welcome_message = """
<b>🎉 Welcome to the Telegram Notifications Service!</b>

Hello! You have been successfully registered for notifications.

<b>Available features:</b>
• Task notifications
• System alerts
• Custom messages

<b>Your registration is complete!</b>
You will now receive notifications when tasks are sent via API.

<i>Service is running and ready to send notifications.</i>
        """
        
        success = send_message(chat_id, welcome_message)
        
        if success:
            print("✅ Response sent successfully!")
            print("\nNow you can test the notification system:")
            print("1. The user is registered")
            print("2. Send notifications via API")
            print("3. User will receive them in Telegram")
        else:
            print("❌ Failed to send response")
    else:
        print("❌ No chat ID found. Send /start to the bot first.")

if __name__ == "__main__":
    main()