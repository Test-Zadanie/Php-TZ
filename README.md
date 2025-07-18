# Telegram Notifications Service

Laravel-based service for receiving tasks from external API and sending notifications to users via Telegram bot.

## Requirements

- PHP 8.0+
- Laravel 9-12
- MySQL/PostgreSQL
- Telegram Bot Token

## Installation

### Manual Installation

1. Copy environment file:
```bash
cp .env.example .env
```

2. Configure database in `.env`:
```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=telegram_notifications
DB_USERNAME=root
DB_PASSWORD=
```

3. Add Telegram bot token to `.env`:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_WEBHOOK_URL=https://yourapp.com/api/telegram/webhook
```

4. Install dependencies:
```bash
composer install
```

5. Generate application key:
```bash
php artisan key:generate
```

6. Run migrations:
```bash
php artisan migrate
```

7. Run seeders:
```bash
php artisan db:seed --class=UserSeeder
```

8. Start the application:
```bash
php artisan serve
```

9. Start queue worker:
```bash
php artisan queue:work
```

### Docker Installation

1. Build and start services:
```bash
docker-compose up -d
```

2. Install dependencies:
```bash
docker-compose exec app composer install
```

3. Generate application key:
```bash
docker-compose exec app php artisan key:generate
```

4. Run migrations:
```bash
docker-compose exec app php artisan migrate
```

5. Run seeders:
```bash
docker-compose exec app php artisan db:seed --class=UserSeeder
```

## Telegram Bot Setup

1. Create bot via @BotFather
2. Get token and add to `.env`
3. Set webhook:
```bash
curl -X POST "https://api.telegram.org/bot{YOUR_BOT_TOKEN}/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://yourapp.com/api/telegram/webhook"}'
```

## Database Structure

### Table `users`
- `id` - User ID
- `name` - User name
- `telegram_id` - Telegram ID (unique)
- `subscribed` - Subscribed to notifications (boolean)

## API Endpoints

### Telegram Webhook
```
POST /api/telegram/webhook
```

### Receive Tasks from External API
```
POST /api/v1/tasks
```

Example request:
```json
{
  "tasks": [
    {
      "title": "Important task",
      "description": "Task description",
      "priority": "high",
      "due_date": "2024-12-31"
    }
  ]
}
```

### Fetch Tasks from External API
```
GET /api/v1/tasks/fetch
```

## Bot Commands

- `/start` - User registration or resubscription

## Usage Example

1. User sends `/start` to bot
2. Bot saves user to database
3. External API sends tasks to `/api/v1/tasks`
4. System adds tasks to queue
5. Notifications are sent to all subscribed users

## Architecture

- **TelegramController** - handles Telegram webhooks
- **ApiController** - receives tasks from external API
- **TelegramService** - works with Telegram Bot API
- **SendNotificationJob** - asynchronous notification sending
- **User Model** - user model with search methods

## Testing

Run tests:
```bash
php artisan test
```

## API Documentation

Import Postman collection from `docs/postman_collection.json`

## Monitoring

All actions are logged in Laravel Log. To view logs:
```bash
tail -f storage/logs/laravel.log
```