<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use HasFactory, Notifiable;

    /**
     * The attributes that are mass assignable.
     */
    protected $fillable = [
        'name',
        'telegram_id',
        'subscribed',
    ];

    /**
     * The attributes that should be cast.
     */
    protected $casts = [
        'subscribed' => 'boolean',
    ];

    /**
     * Get subscribed users for notifications
     */
    public static function getSubscribedUsers()
    {
        return self::where('subscribed', true)->get();
    }

    /**
     * Find user by telegram_id
     */
    public static function findByTelegramId(string $telegramId)
    {
        return self::where('telegram_id', $telegramId)->first();
    }
}