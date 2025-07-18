<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;
use App\Services\TelegramService;
use Illuminate\Support\Facades\Log;

class TelegramController extends Controller
{
    private TelegramService $telegramService;

    public function __construct(TelegramService $telegramService)
    {
        $this->telegramService = $telegramService;
    }

    /**
     * Handle webhook from Telegram
     */
    public function webhook(Request $request)
    {
        try {
            $update = $request->all();
            
            if (isset($update['message'])) {
                $this->handleMessage($update['message']);
            }

            return response()->json(['status' => 'ok']);
        } catch (\Exception $e) {
            Log::error('Telegram webhook error: ' . $e->getMessage());
            return response()->json(['error' => 'Internal error'], 500);
        }
    }

    /**
     * Handle incoming message
     */
    private function handleMessage(array $message): void
    {
        $chatId = $message['chat']['id'];
        $text = $message['text'] ?? '';
        $firstName = $message['from']['first_name'] ?? 'User';
        $lastName = $message['from']['last_name'] ?? '';
        $fullName = trim($firstName . ' ' . $lastName);

        switch ($text) {
            case '/start':
                $this->handleStartCommand($chatId, $fullName);
                break;
            default:
                $this->telegramService->sendMessage($chatId, 'Unknown command. Use /start to register.');
                break;
        }
    }

    /**
     * Handle /start command
     */
    private function handleStartCommand(string $chatId, string $name): void
    {
        $user = User::findByTelegramId($chatId);

        if ($user) {
            $message = "Welcome back, {$user->name}! You are already registered.";
            if (!$user->subscribed) {
                $user->update(['subscribed' => true]);
                $message .= " You have been resubscribed to notifications.";
            }
        } else {
            User::create([
                'name' => $name,
                'telegram_id' => $chatId,
                'subscribed' => true,
            ]);
            $message = "Hello {$name}! You have been successfully registered for notifications.";
        }

        $this->telegramService->sendMessage($chatId, $message);
    }
}