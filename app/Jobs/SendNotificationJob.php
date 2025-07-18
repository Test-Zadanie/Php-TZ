<?php

namespace App\Jobs;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use App\Models\User;
use App\Services\TelegramService;
use Illuminate\Support\Facades\Log;

class SendNotificationJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    private string $message;
    private ?string $telegramId;

    /**
     * Create a new job instance
     */
    public function __construct(string $message, ?string $telegramId = null)
    {
        $this->message = $message;
        $this->telegramId = $telegramId;
    }

    /**
     * Execute the job
     */
    public function handle(TelegramService $telegramService): void
    {
        try {
            if ($this->telegramId) {
                // Send to specific user
                $telegramService->sendMessage($this->telegramId, $this->message);
                Log::info("Notification sent to user: {$this->telegramId}");
            } else {
                // Send to all subscribed users
                $users = User::getSubscribedUsers();
                
                foreach ($users as $user) {
                    $telegramService->sendMessage($user->telegram_id, $this->message);
                    Log::info("Notification sent to user: {$user->telegram_id}");
                }
            }
        } catch (\Exception $e) {
            Log::error("Failed to send notification: " . $e->getMessage());
            throw $e;
        }
    }
}