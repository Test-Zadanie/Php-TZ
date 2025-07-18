<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithFaker;
use Tests\TestCase;
use App\Models\User;
use App\Services\TelegramService;
use Mockery;

class TelegramWebhookTest extends TestCase
{
    use RefreshDatabase;

    public function test_start_command_creates_new_user()
    {
        // Mock TelegramService
        $telegramService = Mockery::mock(TelegramService::class);
        $telegramService->shouldReceive('sendMessage')
            ->once()
            ->with('123456789', Mockery::type('string'))
            ->andReturn(true);

        $this->app->instance(TelegramService::class, $telegramService);

        $webhookData = [
            'message' => [
                'chat' => ['id' => '123456789'],
                'text' => '/start',
                'from' => [
                    'first_name' => 'Test',
                    'last_name' => 'User'
                ]
            ]
        ];

        $response = $this->postJson('/api/telegram/webhook', $webhookData);

        $response->assertStatus(200);
        $response->assertJson(['status' => 'ok']);

        $this->assertDatabaseHas('users', [
            'telegram_id' => '123456789',
            'name' => 'Test User',
            'subscribed' => true
        ]);
    }

    public function test_start_command_resubscribes_existing_user()
    {
        // Create existing unsubscribed user
        User::create([
            'name' => 'Existing User',
            'telegram_id' => '987654321',
            'subscribed' => false
        ]);

        // Mock TelegramService
        $telegramService = Mockery::mock(TelegramService::class);
        $telegramService->shouldReceive('sendMessage')
            ->once()
            ->with('987654321', Mockery::type('string'))
            ->andReturn(true);

        $this->app->instance(TelegramService::class, $telegramService);

        $webhookData = [
            'message' => [
                'chat' => ['id' => '987654321'],
                'text' => '/start',
                'from' => [
                    'first_name' => 'Existing',
                    'last_name' => 'User'
                ]
            ]
        ];

        $response = $this->postJson('/api/telegram/webhook', $webhookData);

        $response->assertStatus(200);

        $this->assertDatabaseHas('users', [
            'telegram_id' => '987654321',
            'subscribed' => true
        ]);
    }

    public function test_stop_command_unsubscribes_existing_user()
    {
        // Create existing subscribed user
        User::create([
            'name' => 'Existing User',
            'telegram_id' => '555666777',
            'subscribed' => true
        ]);

        // Mock TelegramService
        $telegramService = Mockery::mock(TelegramService::class);
        $telegramService->shouldReceive('sendMessage')
            ->once()
            ->with('555666777', Mockery::type('string'))
            ->andReturn(true);

        $this->app->instance(TelegramService::class, $telegramService);

        $webhookData = [
            'message' => [
                'chat' => ['id' => '555666777'],
                'text' => '/stop',
                'from' => [
                    'first_name' => 'Existing',
                    'last_name' => 'User'
                ]
            ]
        ];

        $response = $this->postJson('/api/telegram/webhook', $webhookData);

        $response->assertStatus(200);

        $this->assertDatabaseHas('users', [
            'telegram_id' => '555666777',
            'subscribed' => false
        ]);
    }

    public function test_stop_command_handles_non_existing_user()
    {
        // Mock TelegramService
        $telegramService = Mockery::mock(TelegramService::class);
        $telegramService->shouldReceive('sendMessage')
            ->once()
            ->with('999888777', Mockery::type('string'))
            ->andReturn(true);

        $this->app->instance(TelegramService::class, $telegramService);

        $webhookData = [
            'message' => [
                'chat' => ['id' => '999888777'],
                'text' => '/stop',
                'from' => [
                    'first_name' => 'New',
                    'last_name' => 'User'
                ]
            ]
        ];

        $response = $this->postJson('/api/telegram/webhook', $webhookData);

        $response->assertStatus(200);

        // User should not be created
        $this->assertDatabaseMissing('users', [
            'telegram_id' => '999888777'
        ]);
    }
}