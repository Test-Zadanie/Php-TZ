#!/usr/bin/env python3
"""
Simple test without unicode characters
"""
import urllib.request
import json

def test_connection():
    print("Testing connection to localhost:9000...")
    
    try:
        with urllib.request.urlopen("http://localhost:9000", timeout=5) as response:
            if response.getcode() == 200:
                print("SUCCESS: Server is running!")
                return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False

if __name__ == "__main__":
    print("=== Simple Connection Test ===")
    result = test_connection()
    
    if result:
        print("\nServer is working! You can now:")
        print("1. Open http://localhost:9000 in your browser")
        print("2. Test the webhook endpoint")
        print("3. Use ngrok to expose it to the internet")
    else:
        print("\nServer is not running or not accessible")
        print("Make sure you started: python test_server.py")