#!/usr/bin/env python3
"""
Test script for Telegram notifications API
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_webhook():
    """Test Telegram webhook"""
    print("Testing Telegram webhook...")
    
    # Simulate /start command
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
        response = requests.post(f"{BASE_URL}/api/telegram/webhook", json=webhook_data)
        print(f"Webhook response: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing webhook: {e}")
        return False

def test_tasks_api():
    """Test tasks API"""
    print("\nTesting tasks API...")
    
    tasks_data = {
        "tasks": [
            {
                "title": "Deploy new version",
                "description": "Deploy version 2.1.0 to production server",
                "priority": "high",
                "due_date": "2024-01-15"
            },
            {
                "title": "Database backup",
                "description": "Create backup of production database",
                "priority": "medium",
                "due_date": "2024-01-10"
            }
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/tasks", json=tasks_data)
        print(f"Tasks API response: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing tasks API: {e}")
        return False

def test_home_page():
    """Test home page"""
    print("\nTesting home page...")
    
    try:
        response = requests.get(BASE_URL)
        print(f"Home page response: {response.status_code}")
        if response.status_code == 200:
            print("✓ Home page is accessible")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing home page: {e}")
        return False

def main():
    print("=== Telegram Notifications Service API Test ===\n")
    
    # Wait a moment for server to be ready
    time.sleep(1)
    
    # Test home page
    home_test = test_home_page()
    
    # Test webhook
    webhook_test = test_webhook()
    
    # Test tasks API
    tasks_test = test_tasks_api()
    
    print(f"\n=== Test Results ===")
    print(f"Home page: {'PASS' if home_test else 'FAIL'}")
    print(f"Telegram webhook: {'PASS' if webhook_test else 'FAIL'}")
    print(f"Tasks API: {'PASS' if tasks_test else 'FAIL'}")
    
    if all([home_test, webhook_test, tasks_test]):
        print("\nAll tests passed! Service is working correctly.")
        print("\nNext steps:")
        print("1. Set up ngrok or similar service to expose localhost:8000")
        print("2. Set webhook URL in Telegram: https://your-domain.com/api/telegram/webhook")
        print("3. Test with real Telegram bot by sending /start command")
    else:
        print("\n⚠️  Some tests failed. Check the server logs.")

if __name__ == "__main__":
    main()