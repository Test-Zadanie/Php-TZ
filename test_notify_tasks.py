#!/usr/bin/env python3
"""
Test script for NotifyTasks functionality
"""
import sqlite3
import json
from notify_tasks import fetch_tasks_from_api, filter_tasks, get_subscribed_users, format_tasks_message

def setup_test_database():
    """Create test database with sample users"""
    conn = sqlite3.connect('test_users.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            telegram_id TEXT UNIQUE NOT NULL,
            subscribed BOOLEAN DEFAULT 1
        )
    ''')
    
    # Insert test users
    cursor.execute("DELETE FROM users")  # Clear existing data
    
    cursor.execute("INSERT INTO users (name, telegram_id, subscribed) VALUES (?, ?, ?)",
                   ('Test User 1', '123456789', 1))
    cursor.execute("INSERT INTO users (name, telegram_id, subscribed) VALUES (?, ?, ?)",
                   ('Test User 2', '987654321', 1))
    cursor.execute("INSERT INTO users (name, telegram_id, subscribed) VALUES (?, ?, ?)",
                   ('Unsubscribed User', '555666777', 0))
    
    conn.commit()
    conn.close()
    print("Test database created with sample users")

def test_fetch_tasks():
    """Test fetching tasks from API"""
    print("Testing task fetching...")
    
    tasks = fetch_tasks_from_api()
    
    if tasks:
        print(f"✅ Successfully fetched {len(tasks)} tasks")
        print(f"Sample task: {tasks[0]}")
        return tasks
    else:
        print("❌ Failed to fetch tasks")
        return []

def test_filter_tasks():
    """Test task filtering"""
    print("\nTesting task filtering...")
    
    # Sample tasks for testing
    sample_tasks = [
        {'id': 1, 'userId': 1, 'title': 'Task 1', 'completed': False},
        {'id': 2, 'userId': 2, 'title': 'Task 2', 'completed': True},  # Should be filtered out
        {'id': 3, 'userId': 6, 'title': 'Task 3', 'completed': False},  # Should be filtered out
        {'id': 4, 'userId': 3, 'title': 'Task 4', 'completed': False},
        {'id': 5, 'userId': 5, 'title': 'Task 5', 'completed': False},
    ]
    
    filtered = filter_tasks(sample_tasks)
    
    print(f"Original tasks: {len(sample_tasks)}")
    print(f"Filtered tasks: {len(filtered)}")
    
    expected = 3  # Tasks 1, 4, 5 should pass the filter
    if len(filtered) == expected:
        print(f"✅ Filter working correctly ({expected} tasks passed)")
        return filtered
    else:
        print(f"❌ Filter not working correctly (expected {expected}, got {len(filtered)})")
        return filtered

def test_get_subscribed_users():
    """Test getting subscribed users"""
    print("\nTesting subscribed users retrieval...")
    
    # Temporarily change database name for testing
    import notify_tasks
    original_db = 'users.db'
    notify_tasks.sqlite3.connect = lambda db: sqlite3.connect('test_users.db')
    
    users = get_subscribed_users()
    
    print(f"Found {len(users)} subscribed users")
    for telegram_id, name in users:
        print(f"  - {name} ({telegram_id})")
    
    expected = 2  # Only 2 subscribed users in test data
    if len(users) == expected:
        print(f"✅ User retrieval working correctly ({expected} subscribed users)")
        return users
    else:
        print(f"❌ User retrieval not working correctly (expected {expected}, got {len(users)})")
        return users

def test_format_message():
    """Test message formatting"""
    print("\nTesting message formatting...")
    
    sample_tasks = [
        {'id': 1, 'userId': 1, 'title': 'Complete project documentation', 'completed': False},
        {'id': 2, 'userId': 2, 'title': 'Review code changes', 'completed': False},
    ]
    
    message = format_tasks_message(sample_tasks)
    
    print("Generated message:")
    print("-" * 50)
    print(message)
    print("-" * 50)
    
    if "Complete project documentation" in message and "Review code changes" in message:
        print("✅ Message formatting working correctly")
        return True
    else:
        print("❌ Message formatting not working correctly")
        return False

def main():
    """Run all tests"""
    print("=== Testing NotifyTasks Functionality ===\n")
    
    # Setup test environment
    setup_test_database()
    
    # Test individual components
    tasks = test_fetch_tasks()
    filtered_tasks = test_filter_tasks()
    users = test_get_subscribed_users()
    message_ok = test_format_message()
    
    print(f"\n=== Test Results ===")
    print(f"Task fetching: {'✅ PASS' if tasks else '❌ FAIL'}")
    print(f"Task filtering: {'✅ PASS' if filtered_tasks else '❌ FAIL'}")
    print(f"User retrieval: {'✅ PASS' if users else '❌ FAIL'}")
    print(f"Message formatting: {'✅ PASS' if message_ok else '❌ FAIL'}")
    
    all_pass = all([tasks, filtered_tasks, users, message_ok])
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_pass else '❌ SOME TESTS FAILED'}")
    
    if all_pass:
        print("\n🎉 NotifyTasks functionality is working correctly!")
        print("You can now run: python notify_tasks.py")
    else:
        print("\n⚠️  Some components need debugging")
    
    # Cleanup
    import os
    try:
        os.remove('test_users.db')
        print("\nTest database cleaned up")
    except:
        pass

if __name__ == "__main__":
    main()