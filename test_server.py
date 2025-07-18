#!/usr/bin/env python3
"""
Simple test server for Telegram webhook testing
"""
import json
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import urllib.request
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot Token
BOT_TOKEN = "2143877832:AAGO0ssY0d-d87xrxs3fOOIAno_qg2DVC3k"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Initialize SQLite database
def init_db():
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
            logger.info(f"Message sent to chat {chat_id}: {result}")
            return result.get('ok', False)
    except Exception as e:
        logger.error(f"Error sending message: {e}")
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
        
        send_telegram_message(chat_id, message)
        return True
    except Exception as e:
        logger.error(f"Error handling start command: {e}")
        return False

def handle_stop_command(chat_id, user_name):
    """Handle /stop command"""
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (str(chat_id),))
        user = cursor.fetchone()
        
        if user:
            # User exists, unsubscribe
            cursor.execute("UPDATE users SET subscribed = 0 WHERE telegram_id = ?", (str(chat_id),))
            message = f"You have been unsubscribed from notifications, {user[1]}. Send /start to resubscribe."
        else:
            # User doesn't exist
            message = "You are not registered yet. Send /start to register first."
        
        conn.commit()
        conn.close()
        
        send_telegram_message(chat_id, message)
        return True
    except Exception as e:
        logger.error(f"Error handling stop command: {e}")
        return False

def broadcast_notification(message):
    """Send notification to all subscribed users"""
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT telegram_id FROM users WHERE subscribed = 1")
        users = cursor.fetchall()
        conn.close()
        
        for user in users:
            send_telegram_message(user[0], message)
            
        return len(users)
    except Exception as e:
        logger.error(f"Error broadcasting notification: {e}")
        return 0

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/telegram/webhook':
            # Handle Telegram webhook
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                update = json.loads(post_data.decode())
                logger.info(f"Received update: {update}")
                
                if 'message' in update:
                    message = update['message']
                    chat_id = message['chat']['id']
                    text = message.get('text', '')
                    
                    # Get user name
                    first_name = message.get('from', {}).get('first_name', 'User')
                    last_name = message.get('from', {}).get('last_name', '')
                    full_name = f"{first_name} {last_name}".strip()
                    
                    if text == '/start':
                        handle_start_command(chat_id, full_name)
                    elif text == '/stop':
                        handle_stop_command(chat_id, full_name)
                    else:
                        send_telegram_message(chat_id, "Unknown command. Use /start to register or /stop to unsubscribe.")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok'}).encode())
                
            except Exception as e:
                logger.error(f"Error processing webhook: {e}")
                self.send_response(500)
                self.end_headers()
                
        elif self.path == '/api/v1/tasks':
            # Handle tasks endpoint
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode())
                tasks = data.get('tasks', [])
                
                for task in tasks:
                    title = task.get('title', 'New Task')
                    description = task.get('description', '')
                    priority = task.get('priority', 'normal')
                    due_date = task.get('due_date', '')
                    
                    message = f"<b>🔔 New Task:</b> {title}\n\n"
                    if description:
                        message += f"<b>Description:</b> {description}\n\n"
                    message += f"<b>Priority:</b> {priority.title()}\n"
                    if due_date:
                        message += f"<b>Due Date:</b> {due_date}\n"
                    
                    count = broadcast_notification(message)
                    logger.info(f"Notification sent to {count} users")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'status': 'success',
                    'message': 'Tasks processed successfully',
                    'count': len(tasks)
                }
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                logger.error(f"Error processing tasks: {e}")
                self.send_response(500)
                self.end_headers()
        elif self.path == '/api/v1/notify-tasks':
            # Handle NotifyTasks functionality
            self.handle_notify_tasks()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <html>
            <head><title>Telegram Notifications Service</title></head>
            <body>
                <h1>Telegram Notifications Service</h1>
                <p>Service is running!</p>
                <h2>Available Endpoints:</h2>
                <ul>
                    <li><code>POST /api/telegram/webhook</code> - Telegram webhook</li>
                    <li><code>POST /api/v1/tasks</code> - Send custom tasks</li>
                    <li><code>POST /api/v1/notify-tasks</code> - Trigger NotifyTasks</li>
                </ul>
                <h2>Bot Commands:</h2>
                <ul>
                    <li><code>/start</code> - Register for notifications</li>
                    <li><code>/stop</code> - Unsubscribe from notifications</li>
                </ul>
                <p><strong>Bot:</strong> @TestNewNewTest_bot</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_notify_tasks(self):
        """Handle NotifyTasks API endpoint"""
        try:
            from notify_tasks import notify_tasks
            
            # Run the notify_tasks function
            success = notify_tasks()
            
            if success:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'status': 'success',
                    'message': 'NotifyTasks executed successfully'
                }
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'status': 'error',
                    'message': 'NotifyTasks execution failed'
                }
                self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            logger.error(f"Error in handle_notify_tasks: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'error',
                'message': f'Error: {str(e)}'
            }
            self.wfile.write(json.dumps(response).encode())

def run_server():
    init_db()
    server_address = ('', 9000)
    httpd = HTTPServer(server_address, WebhookHandler)
    logger.info("Server running on http://localhost:9000")
    logger.info("Webhook URL: http://localhost:9000/api/telegram/webhook")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()