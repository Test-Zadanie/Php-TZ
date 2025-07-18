# Quick Start Guide

## How to Run the Project

### Step 1: Start the Server

Open terminal/command prompt and run:
```bash
cd telegram-notifications-service
python test_server.py
```

The server will start on `http://localhost:8080`

### Step 2: Test the Server

In a new terminal window, run:
```bash
python simple_test.py
```

You should see "SUCCESS: Server is running!"

### Step 3: Test in Browser

Open your browser and go to:
```
http://localhost:8080
```

You should see the service homepage.

### Step 4: Test API Endpoints

#### Test Webhook (simulates Telegram bot /start command):
```bash
curl -X POST http://localhost:8080/api/telegram/webhook -H "Content-Type: application/json" -d "{\"message\":{\"chat\":{\"id\":\"123456789\"},\"text\":\"/start\",\"from\":{\"first_name\":\"Test\",\"last_name\":\"User\"}}}"
```

#### Test Tasks API:
```bash
curl -X POST http://localhost:8080/api/v1/tasks -H "Content-Type: application/json" -d "{\"tasks\":[{\"title\":\"Test Task\",\"description\":\"This is a test\",\"priority\":\"high\"}]}"
```

## Setting Up Real Telegram Bot

### Step 1: Expose Local Server to Internet

Install ngrok:
```bash
# Download from https://ngrok.com/
# Then run:
ngrok http 8080
```

This will give you a public URL like `https://abc123.ngrok.io`

### Step 2: Set Telegram Webhook

Replace `YOUR_BOT_TOKEN` with your actual bot token and `YOUR_NGROK_URL` with the ngrok URL:

```bash
curl -X POST "https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook" -H "Content-Type: application/json" -d "{\"url\": \"YOUR_NGROK_URL/api/telegram/webhook\"}"
```

Example:
```bash
curl -X POST "https://api.telegram.org/bot2143877832:AAGO0ssY0d-d87xrxs3fOOIAno_qg2DVC3k/setWebhook" -H "Content-Type: application/json" -d "{\"url\": \"https://abc123.ngrok.io/api/telegram/webhook\"}"
```

### Step 3: Test with Real Telegram Bot

1. Find your bot in Telegram (the one you created with @BotFather)
2. Send `/start` command
3. You should receive a welcome message
4. Check your server logs to see the webhook processing

## Database

The server automatically creates a SQLite database file `users.db` in the project directory. You can inspect it with any SQLite browser.

## Sending Test Notifications

To send a test notification to all registered users:

```bash
curl -X POST http://localhost:8080/api/v1/tasks -H "Content-Type: application/json" -d "{\"tasks\":[{\"title\":\"Hello from API!\",\"description\":\"This is a test notification\",\"priority\":\"high\",\"due_date\":\"2024-01-15\"}]}"
```

## Troubleshooting

### Port 8080 is busy
If port 8080 is already in use, edit `test_server.py` and change the port number:
```python
server_address = ('', 8081)  # Change to different port
```

### Server not responding
Make sure you're in the correct directory and Python is installed:
```bash
cd telegram-notifications-service
python --version
python test_server.py
```

### Webhook not working
1. Check that ngrok is running
2. Verify the webhook URL is set correctly
3. Check server logs for errors
4. Make sure the bot token is correct

## Next Steps

1. Register users by sending `/start` to your bot
2. Test the notification system with the tasks API
3. Integrate with your external systems
4. Deploy to a production server

The service is now ready to receive tasks and send notifications to your Telegram bot users!