#!/usr/bin/env python3
"""
Script to set up Telegram webhook
"""
import urllib.request
import urllib.parse
import json
import sys

BOT_TOKEN = "2143877832:AAGO0ssY0d-d87xrxs3fOOIAno_qg2DVC3k"

def set_webhook(webhook_url):
    """Set webhook for Telegram bot"""
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    
    data = {
        'url': webhook_url
    }
    
    try:
        data_encoded = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(api_url, data=data_encoded)
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('ok'):
                print(f"SUCCESS: Webhook set to {webhook_url}")
                return True
            else:
                print(f"FAILED: {result.get('description', 'Unknown error')}")
                return False
                
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def get_webhook_info():
    """Get current webhook info"""
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    
    try:
        with urllib.request.urlopen(api_url) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('ok'):
                info = result.get('result', {})
                print("Current webhook info:")
                print(f"  URL: {info.get('url', 'Not set')}")
                print(f"  Has custom certificate: {info.get('has_custom_certificate', False)}")
                print(f"  Pending updates: {info.get('pending_update_count', 0)}")
                if info.get('last_error_date'):
                    print(f"  Last error: {info.get('last_error_message', 'Unknown')}")
                return info
            else:
                print(f"FAILED: {result.get('description', 'Unknown error')}")
                return None
                
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def main():
    print("=== Telegram Webhook Setup ===\n")
    
    if len(sys.argv) < 2:
        print("Usage: python setup_webhook.py <webhook_url>")
        print("Example: python setup_webhook.py https://abc123.ngrok.io/api/telegram/webhook")
        print("\nOr use 'info' to get current webhook info:")
        print("python setup_webhook.py info")
        return
    
    command = sys.argv[1]
    
    if command == "info":
        get_webhook_info()
    elif command.startswith("http"):
        webhook_url = command
        if not webhook_url.endswith("/api/telegram/webhook"):
            webhook_url += "/api/telegram/webhook"
        
        print(f"Setting webhook to: {webhook_url}")
        success = set_webhook(webhook_url)
        
        if success:
            print("\nWebhook set successfully!")
            print("Now you can:")
            print("1. Send /start to your bot")
            print("2. Check server logs for webhook requests")
            print("3. Test the notification system")
        else:
            print("\nFailed to set webhook. Check your bot token and URL.")
    else:
        print("Invalid command. Use a URL or 'info'")

if __name__ == "__main__":
    main()