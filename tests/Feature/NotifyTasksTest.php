<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\User;
use App\Console\Commands\NotifyTasks;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Queue;
use App\Jobs\SendNotificationJob;

class NotifyTasksTest extends TestCase
{
    use RefreshDatabase;

    public function test_notify_tasks_command_filters_and_sends_notifications()
    {
        Queue::fake();
        
        // Create test users
        $subscribedUser = User::create([
            'name' => 'Subscribed User',
            'telegram_id' => '123456789',
            'subscribed' => true
        ]);
        
        $unsubscribedUser = User::create([
            'name' => 'Unsubscribed User',
            'telegram_id' => '987654321',
            'subscribed' => false
        ]);

        // Mock external API response
        Http::fake([
            'jsonplaceholder.typicode.com/todos' => Http::response([
                [
                    'id' => 1,
                    'userId' => 1,
                    'title' => 'Test task 1',
                    'completed' => false
                ],
                [
                    'id' => 2,
                    'userId' => 2,
                    'title' => 'Test task 2',
                    'completed' => true // Should be filtered out
                ],
                [
                    'id' => 3,
                    'userId' => 6,
                    'title' => 'Test task 3',
                    'completed' => false // Should be filtered out (userId > 5)
                ],
                [
                    'id' => 4,
                    'userId' => 3,
                    'title' => 'Test task 4',
                    'completed' => false
                ]
            ])
        ]);

        // Run the command
        $this->artisan('notify:tasks')
            ->expectsOutput('Starting task notification process...')
            ->expectsOutput('Found 2 tasks matching criteria')
            ->expectsOutput('Found 1 subscribed users')
            ->expectsOutput('Task notification process completed successfully')
            ->assertExitCode(0);

        // Assert notification job was dispatched only to subscribed user
        Queue::assertPushed(SendNotificationJob::class, function ($job) use ($subscribedUser) {
            return $job->telegramId === $subscribedUser->telegram_id;
        });

        // Assert job was not dispatched to unsubscribed user
        Queue::assertNotPushed(SendNotificationJob::class, function ($job) use ($unsubscribedUser) {
            return $job->telegramId === $unsubscribedUser->telegram_id;
        });
    }

    public function test_notify_tasks_handles_no_tasks()
    {
        // Mock API response with no matching tasks
        Http::fake([
            'jsonplaceholder.typicode.com/todos' => Http::response([
                [
                    'id' => 1,
                    'userId' => 1,
                    'title' => 'Completed task',
                    'completed' => true
                ]
            ])
        ]);

        $this->artisan('notify:tasks')
            ->expectsOutput('No tasks to notify about')
            ->assertExitCode(0);
    }

    public function test_notify_tasks_handles_no_subscribed_users()
    {
        // Create only unsubscribed user
        User::create([
            'name' => 'Unsubscribed User',
            'telegram_id' => '123456789',
            'subscribed' => false
        ]);

        Http::fake([
            'jsonplaceholder.typicode.com/todos' => Http::response([
                [
                    'id' => 1,
                    'userId' => 1,
                    'title' => 'Test task',
                    'completed' => false
                ]
            ])
        ]);

        $this->artisan('notify:tasks')
            ->expectsOutput('No subscribed users to notify')
            ->assertExitCode(0);
    }
}