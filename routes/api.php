<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\TelegramController;
use App\Http\Controllers\ApiController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
*/

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');

// Telegram webhook route
Route::post('/telegram/webhook', [TelegramController::class, 'webhook']);

// API routes for external integration
Route::prefix('api/v1')->group(function () {
    Route::post('/tasks', [ApiController::class, 'receiveTasks']);
    Route::get('/tasks/fetch', [ApiController::class, 'fetchExternalTasks']);
});