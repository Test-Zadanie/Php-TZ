#!/usr/bin/env python3
"""
NotifyTasks - Fetch tasks from external API and notify users
"""
import urllib.request
import urllib.parse
import json
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot Token
BOT_TOKEN = "2143877832:AAGO0ssY0d-d87xrxs3fOOIAno_qg2DVC3k"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def fetch_tasks_from_api():
    """Fetch tasks from jsonplaceholder API"""
    try:
        with urllib.request.urlopen("https://jsonplaceholder.typicode.com/todos") as response:
            tasks = json.loads(response.read().decode())
            logger.info(f"Fetched {len(tasks)} tasks from API")
            return tasks
    except Exception as e:
        logger.error(f"Error fetching tasks: {e}")
        return []

def filter_tasks(tasks):
    """Filter tasks: completed = false and userId <= 5"""
    filtered = []
    for task in tasks:
        if task.get('completed') is False and task.get('userId', 0) <= 5:
            filtered.append(task)
    
    logger.info(f"Filtered to {len(filtered)} tasks matching criteria")
    return filtered

def get_subscribed_users():
    """Get all subscribed users from database"""
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT telegram_id, name FROM users WHERE subscribed = 1")
        users = cursor.fetchall()
        conn.close()
        
        logger.info(f"Found {len(users)} subscribed users")
        return users
    except Exception as e:
        logger.error(f"Error getting subscribed users: {e}")
        return []

def send_telegram_message(chat_id, message):
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
        logger.error(f"Error sending message to {chat_id}: {e}")
        return False

def format_tasks_message(tasks):
    """Format tasks into a message"""
    if not tasks:
        return "No tasks found matching criteria."
    
    message = "<b>📋 New Tasks Available</b>\n\n"
    message += f"Found {len(tasks)} incomplete tasks:\n\n"
    
    for index, task in enumerate(tasks[:10]):  # Limit to first 10 tasks
        task_number = index + 1
        message += f"<b>{task_number}. {task['title']}</b>\n"
        message += f"   User ID: {task['userId']}\n"
        message += f"   Task ID: {task['id']}\n"
        message += f"   Status: ⏳ Pending\n\n"
    
    if len(tasks) > 10:
        message += f"... and {len(tasks) - 10} more tasks\n\n"
    
    message += "💡 <i>These tasks are waiting to be completed</i>"
    
    return message

def notify_tasks():
    """Main function to fetch tasks and notify users"""
    logger.info("Starting task notification process...")
    
    # Fetch tasks from API
    all_tasks = fetch_tasks_from_api()
    if not all_tasks:
        logger.error("No tasks fetched from API")
        return False
    
    # Filter tasks
    filtered_tasks = filter_tasks(all_tasks)
    if not filtered_tasks:
        logger.info("No tasks match the criteria")
        return True
    
    # Get subscribed users
    users = get_subscribed_users()
    if not users:
        logger.info("No subscribed users to notify")
        return True
    
    # Format message
    message = format_tasks_message(filtered_tasks)
    
    # Send notifications
    success_count = 0
    for telegram_id, name in users:
        if send_telegram_message(telegram_id, message):
            logger.info(f"Notification sent to {name} ({telegram_id})")
            success_count += 1
        else:
            logger.error(f"Failed to send notification to {name} ({telegram_id})")
    
    logger.info(f"Task notification process completed. Sent {success_count}/{len(users)} notifications")
    return True

if __name__ == "__main__":
    print("=== NotifyTasks - Task Notification System ===")
    print("Fetching tasks from jsonplaceholder API...")
    print("Filtering tasks (completed=false, userId<=5)...")
    print("Notifying subscribed users...")
    
    success = notify_tasks()
    
    if success:
        print("✅ Task notification process completed successfully!")
    else:
        print("❌ Task notification process failed!")
    
    print("\nTo run this regularly:")
    print("1. Set up a cron job: */30 * * * * python notify_tasks.py")
    print("2. Or run manually: python notify_tasks.py")
    print("3. Check logs for detailed information")