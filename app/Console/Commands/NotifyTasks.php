<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use App\Models\User;
use App\Jobs\SendNotificationJob;

class NotifyTasks extends Command
{
    /**
     * The name and signature of the console command.
     */
    protected $signature = 'notify:tasks';

    /**
     * The console command description.
     */
    protected $description = 'Fetch tasks from external API and notify subscribed users';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        $this->info('Starting task notification process...');

        try {
            // Fetch tasks from external API
            $this->info('Fetching tasks from jsonplaceholder API...');
            $response = Http::get('https://jsonplaceholder.typicode.com/todos');

            if (!$response->successful()) {
                $this->error('Failed to fetch tasks from API');
                return Command::FAILURE;
            }

            $allTasks = $response->json();
            $this->info('Fetched ' . count($allTasks) . ' tasks');

            // Filter tasks: completed = false and userId <= 5
            $filteredTasks = collect($allTasks)->filter(function ($task) {
                return $task['completed'] === false && $task['userId'] <= 5;
            });

            $this->info('Found ' . $filteredTasks->count() . ' tasks matching criteria');

            if ($filteredTasks->isEmpty()) {
                $this->info('No tasks to notify about');
                return Command::SUCCESS;
            }

            // Get subscribed users
            $subscribedUsers = User::getSubscribedUsers();
            $this->info('Found ' . $subscribedUsers->count() . ' subscribed users');

            if ($subscribedUsers->isEmpty()) {
                $this->info('No subscribed users to notify');
                return Command::SUCCESS;
            }

            // Format tasks message
            $message = $this->formatTasksMessage($filteredTasks->toArray());

            // Send notifications to each subscribed user via queue
            foreach ($subscribedUsers as $user) {
                SendNotificationJob::dispatch($message, $user->telegram_id);
                $this->info("Queued notification for user: {$user->name}");
            }

            $this->info('Task notification process completed successfully');
            Log::info('NotifyTasks command executed successfully', [
                'total_tasks' => count($allTasks),
                'filtered_tasks' => $filteredTasks->count(),
                'notified_users' => $subscribedUsers->count()
            ]);

            return Command::SUCCESS;
        } catch (\Exception $e) {
            $this->error('Error: ' . $e->getMessage());
            Log::error('NotifyTasks command failed', ['error' => $e->getMessage()]);
            return Command::FAILURE;
        }
    }

    /**
     * Format tasks into message
     */
    private function formatTasksMessage(array $tasks): string
    {
        $message = "<b>📋 New Tasks Available</b>\n\n";
        $message .= "Found " . count($tasks) . " incomplete tasks:\n\n";

        foreach ($tasks as $index => $task) {
            $taskNumber = $index + 1;
            $message .= "<b>{$taskNumber}. {$task['title']}</b>\n";
            $message .= "   User ID: {$task['userId']}\n";
            $message .= "   Task ID: {$task['id']}\n";
            $message .= "   Status: ⏳ Pending\n\n";
        }

        $message .= "💡 <i>These tasks are waiting to be completed</i>";

        return $message;
    }
}