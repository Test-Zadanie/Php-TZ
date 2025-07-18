<?php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;

class UserModelTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_be_created_with_telegram_id()
    {
        $user = User::create([
            'name' => 'Test User',
            'telegram_id' => '123456789',
            'subscribed' => true
        ]);

        $this->assertNotNull($user->id);
        $this->assertEquals('Test User', $user->name);
        $this->assertEquals('123456789', $user->telegram_id);
        $this->assertTrue($user->subscribed);
    }

    public function test_find_by_telegram_id_returns_correct_user()
    {
        $user = User::create([
            'name' => 'Test User',
            'telegram_id' => '123456789',
            'subscribed' => true
        ]);

        $foundUser = User::findByTelegramId('123456789');

        $this->assertNotNull($foundUser);
        $this->assertEquals($user->id, $foundUser->id);
        $this->assertEquals('Test User', $foundUser->name);
    }

    public function test_get_subscribed_users_returns_only_subscribed()
    {
        User::create([
            'name' => 'Subscribed User',
            'telegram_id' => '111111111',
            'subscribed' => true
        ]);

        User::create([
            'name' => 'Unsubscribed User',
            'telegram_id' => '222222222',
            'subscribed' => false
        ]);

        $subscribedUsers = User::getSubscribedUsers();

        $this->assertCount(1, $subscribedUsers);
        $this->assertEquals('Subscribed User', $subscribedUsers->first()->name);
    }
}