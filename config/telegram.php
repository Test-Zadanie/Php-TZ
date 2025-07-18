<?php

return [
    /*
    |--------------------------------------------------------------------------
    | Telegram Bot Token
    |--------------------------------------------------------------------------
    |
    | Your Telegram Bot Token from BotFather
    |
    */
    'bot_token' => env('TELEGRAM_BOT_TOKEN', ''),

    /*
    |--------------------------------------------------------------------------
    | Webhook URL
    |--------------------------------------------------------------------------
    |
    | URL for Telegram webhook
    |
    */
    'webhook_url' => env('TELEGRAM_WEBHOOK_URL', ''),

    /*
    |--------------------------------------------------------------------------
    | External API Configuration
    |--------------------------------------------------------------------------
    |
    | Configuration for external API integration
    |
    */
    'external_api_url' => env('EXTERNAL_API_URL', 'https://jsonplaceholder.typicode.com/todos'),
    
    /*
    |--------------------------------------------------------------------------
    | Queue Configuration
    |--------------------------------------------------------------------------
    |
    | Queue settings for notification processing
    |
    */
    'queue' => [
        'connection' => env('QUEUE_CONNECTION', 'database'),
        'queue' => env('NOTIFICATION_QUEUE', 'default'),
    ],
];