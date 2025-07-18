<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\User;

class UserSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        User::create([
            'name' => 'Test User 1',
            'telegram_id' => '123456789',
            'subscribed' => true,
        ]);

        User::create([
            'name' => 'Test User 2',
            'telegram_id' => '987654321',
            'subscribed' => true,
        ]);

        User::create([
            'name' => 'Unsubscribed User',
            'telegram_id' => '555666777',
            'subscribed' => false,
        ]);
    }
}