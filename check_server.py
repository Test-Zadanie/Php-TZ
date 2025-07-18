#!/usr/bin/env python3
"""
Simple server status checker
"""
import urllib.request
import json
import time

def check_server():
    print("Checking server status...")
    
    try:
        # Test home page
        with urllib.request.urlopen("http://localhost:8000") as response:
            if response.getcode() == 200:
                print("✓ Server is running on http://localhost:8000")
                return True
    except Exception as e:
        print(f"✗ Server is not responding: {e}")
        return False

def test_webhook():
    print("\nTesting webhook endpoint...")
    
    webhook_data = {
        "message": {
            "chat": {"id": "123456789"},
            "text": "/start",
            "from": {
                "first_name": "Test",
                "last_name": "User"
            }
        }
    }
    
    try:
        data = json.dumps(webhook_data).encode('utf-8')
        req = urllib.request.Request(
            "http://localhost:8000/api/telegram/webhook",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')
            print(f"✓ Webhook test successful: {result}")
            return True
    except Exception as e:
        print(f"✗ Webhook test failed: {e}")
        return False

def test_tasks_api():
    print("\nTesting tasks API endpoint...")
    
    tasks_data = {
        "tasks": [
            {
                "title": "Test Task",
                "description": "This is a test task",
                "priority": "high",
                "due_date": "2024-01-15"
            }
        ]
    }
    
    try:
        data = json.dumps(tasks_data).encode('utf-8')
        req = urllib.request.Request(
            "http://localhost:8000/api/v1/tasks",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')
            print(f"✓ Tasks API test successful: {result}")
            return True
    except Exception as e:
        print(f"✗ Tasks API test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Telegram Notifications Service Test ===\n")
    
    # Check server status
    server_ok = check_server()
    
    if server_ok:
        # Test webhook
        webhook_ok = test_webhook()
        
        # Test tasks API
        tasks_ok = test_tasks_api()
        
        print(f"\n=== Summary ===")
        print(f"Server: {'PASS' if server_ok else 'FAIL'}")
        print(f"Webhook: {'PASS' if webhook_ok else 'FAIL'}")
        print(f"Tasks API: {'PASS' if tasks_ok else 'FAIL'}")
        
        if all([server_ok, webhook_ok, tasks_ok]):
            print("\n🎉 All tests passed!")
            print("\nYour Telegram bot is ready to use!")
            print("Next steps:")
            print("1. Use ngrok to expose localhost:8000 to the internet")
            print("2. Set webhook in Telegram bot")
            print("3. Send /start to your bot to test")
        else:
            print("\n⚠️ Some tests failed")
    else:
        print("\n❌ Server is not running. Please start the server first.")
        print("Run: python test_server.py")