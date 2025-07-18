#!/usr/bin/env python3
"""
Test API calls
"""
import urllib.request
import json

def test_webhook():
    """Test webhook endpoint"""
    print("Testing webhook endpoint...")
    
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
            "http://localhost:9000/api/telegram/webhook",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')
            print(f"Webhook response: {result}")
            return True
    except Exception as e:
        print(f"Webhook failed: {e}")
        return False

def test_tasks():
    """Test tasks API"""
    print("\nTesting tasks API...")
    
    tasks_data = {
        "tasks": [
            {
                "title": "Test Notification",
                "description": "This is a test notification from the API",
                "priority": "high",
                "due_date": "2024-01-15"
            }
        ]
    }
    
    try:
        data = json.dumps(tasks_data).encode('utf-8')
        req = urllib.request.Request(
            "http://localhost:9000/api/v1/tasks",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')
            print(f"Tasks API response: {result}")
            return True
    except Exception as e:
        print(f"Tasks API failed: {e}")
        return False

if __name__ == "__main__":
    print("=== API Test ===")
    
    webhook_ok = test_webhook()
    tasks_ok = test_tasks()
    
    print(f"\n=== Results ===")
    print(f"Webhook: {'PASS' if webhook_ok else 'FAIL'}")
    print(f"Tasks API: {'PASS' if tasks_ok else 'FAIL'}")
    
    if webhook_ok and tasks_ok:
        print("\nAll API tests passed!")
        print("Your Telegram bot service is ready!")
    else:
        print("\nSome tests failed. Check server logs.")