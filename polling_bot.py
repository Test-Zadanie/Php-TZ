#!/usr/bin/env python3
"""
Polling-based Telegram bot (alternative to webhook)
"""
import urllib.request
import urllib.parse
import json
import time
import sqlite3

BOT_TOKEN = "2143877832:AAGO0ssY0d-d87xrxs3fOOIAno_qg2DVC3k"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def init_db():
    """Initialize database"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            telegram_id TEXT UNIQUE NOT NULL,
            subscribed BOOLEAN DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

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
        print(f"Error sending message: {e}")
        return False

def handle_start_command(chat_id, user_name):
    """Handle /start command"""
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (str(chat_id),))
        user = cursor.fetchone()
        
        if user:
            # User exists, resubscribe if needed
            cursor.execute("UPDATE users SET subscribed = 1 WHERE telegram_id = ?", (str(chat_id),))
            message = f"Welcome back, {user[1]}! You are now subscribed to notifications."
        else:
            # Create new user
            cursor.execute("INSERT INTO users (name, telegram_id, subscribed) VALUES (?, ?, 1)", 
                         (user_name, str(chat_id)))
            message = f"Hello {user_name}! You have been successfully registered for notifications."
        
        conn.commit()
        conn.close()
        
        send_message(chat_id, message)
        print(f"Processed /start from {user_name} (ID: {chat_id})")
        return True
    except Exception as e:
        print(f"Error handling start command: {e}")
        return False

def get_updates(offset=0):
    """Get updates from Telegram"""
    try:
        params = {
            'offset': offset,
            'timeout': 30,
            'allowed_updates': ['message']
        }
        
        url = f"{TELEGRAM_API_URL}/getUpdates?" + urllib.parse.urlencode(params)
        
        with urllib.request.urlopen(url) as response:
            result = json.loads(response.read().decode())
            return result.get('result', [])
    except Exception as e:
        print(f"Error getting updates: {e}")
        return []

def run_polling_bot():
    """Run bot in polling mode"""
    print("Starting Telegram bot in polling mode...")
    print("Bot: @TestNewNewTest_bot")
    print("Send /start to test!")
    print("Press Ctrl+C to stop")
    
    init_db()
    offset = 0
    
    try:
        while True:
            updates = get_updates(offset)
            
            for update in updates:
                offset = update['update_id'] + 1
                
                if 'message' in update:
                    message = update['message']
                    chat_id = message['chat']['id']
                    text = message.get('text', '')
                    
                    # Get user name
                    user_info = message.get('from', {})
                    first_name = user_info.get('first_name', 'User')
                    last_name = user_info.get('last_name', '')
                    full_name = f"{first_name} {last_name}".strip()
                    
                    print(f"Received message: '{text}' from {full_name}")
                    
                    if text == '/start':
                        handle_start_command(chat_id, full_name)
                    else:
                        send_message(chat_id, "Unknown command. Use /start to register.")
            
            time.sleep(1)  # Short pause between requests
            
    except KeyboardInterrupt:
        print("\nBot stopped.")
    except Exception as e:
        print(f"Error in polling loop: {e}")

if __name__ == "__main__":
    run_polling_bot()