<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class TelegramService
{
    private string $botToken;
    private string $apiUrl;

    public function __construct()
    {
        $this->botToken = config('telegram.bot_token');
        $this->apiUrl = "https://api.telegram.org/bot{$this->botToken}";
    }

    /**
     * Send message to Telegram user
     */
    public function sendMessage(string $chatId, string $message): bool
    {
        try {
            $response = Http::post("{$this->apiUrl}/sendMessage", [
                'chat_id' => $chatId,
                'text' => $message,
                'parse_mode' => 'HTML'
            ]);

            if ($response->successful()) {
                Log::info("Message sent to chat {$chatId}");
                return true;
            }

            Log::error("Failed to send message to chat {$chatId}: " . $response->body());
            return false;
        } catch (\Exception $e) {
            Log::error("Telegram API error: " . $e->getMessage());
            return false;
        }
    }

    /**
     * Get updates from Telegram
     */
    public function getUpdates(int $offset = 0): array
    {
        try {
            $response = Http::get("{$this->apiUrl}/getUpdates", [
                'offset' => $offset,
                'timeout' => 30
            ]);

            if ($response->successful()) {
                return $response->json()['result'] ?? [];
            }

            Log::error("Failed to get updates: " . $response->body());
            return [];
        } catch (\Exception $e) {
            Log::error("Telegram API error: " . $e->getMessage());
            return [];
        }
    }

    /**
     * Set webhook for bot
     */
    public function setWebhook(string $url): bool
    {
        try {
            $response = Http::post("{$this->apiUrl}/setWebhook", [
                'url' => $url
            ]);

            return $response->successful();
        } catch (\Exception $e) {
            Log::error("Failed to set webhook: " . $e->getMessage());
            return false;
        }
    }
}