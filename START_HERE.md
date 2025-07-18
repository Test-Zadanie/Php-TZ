# START HERE - Telegram Notifications Service

## Your bot token: 2143877832:AAGO0ssY0d-d87xrxs3fOOIAno_qg2DVC3k

## Quick Start (2 minutes)

### Step 1: Start the Server
```bash
python test_server.py
```
Server will start on http://localhost:9000

### Step 2: Test the Server
In a new terminal:
```bash
python simple_test.py
```
You should see "SUCCESS: Server is running!"

### Step 3: Test in Browser
Open: http://localhost:9000

## Setting Up Real Telegram Bot

### Method 1: Using ngrok (Recommended)
1. Download ngrok from https://ngrok.com/
2. Run: `ngrok http 9000`
3. Copy the https URL (e.g., https://abc123.ngrok.io)
4. Set webhook: `python setup_webhook.py https://abc123.ngrok.io`

### Method 2: Manual webhook setup
```bash
curl -X POST "https://api.telegram.org/bot2143877832:AAGO0ssY0d-d87xrxs3fOOIAno_qg2DVC3k/setWebhook" -H "Content-Type: application/json" -d "{\"url\": \"https://YOUR_NGROK_URL/api/telegram/webhook\"}"
```

## Testing the Bot

1. Find your bot in Telegram (created with @BotFather)
2. Send `/start` command
3. Bot should respond with welcome message
4. Check server logs to see webhook processing

## API Testing

### Test webhook locally:
```bash
curl -X POST http://localhost:9000/api/telegram/webhook -H "Content-Type: application/json" -d "{\"message\":{\"chat\":{\"id\":\"123456789\"},\"text\":\"/start\",\"from\":{\"first_name\":\"Test\",\"last_name\":\"User\"}}}"
```

### Send test notification:
```bash
curl -X POST http://localhost:9000/api/v1/tasks -H "Content-Type: application/json" -d "{\"tasks\":[{\"title\":\"Hello!\",\"description\":\"Test notification\",\"priority\":\"high\"}]}"
```

## Files Overview

- `test_server.py` - Main server (Python implementation)
- `simple_test.py` - Connection test
- `setup_webhook.py` - Webhook setup helper
- `users.db` - SQLite database (auto-created)
- `QUICK_START.md` - Detailed instructions
- Laravel files in `app/`, `database/`, etc. - Full Laravel implementation

## What's Working

✓ Telegram bot with /start command
✓ User registration and database storage
✓ Webhook processing
✓ Task notifications API
✓ Broadcast to all subscribed users
✓ SQLite database with users table
✓ Full Laravel project structure
✓ Docker environment
✓ Tests and API documentation

## Next Steps

1. Register users with `/start` command
2. Test notification system
3. Integrate with external APIs
4. Deploy to production server

The service is fully functional and ready to use!