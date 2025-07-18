<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Jobs\SendNotificationJob;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class ApiController extends Controller
{
    /**
     * Receive tasks from external API and send notifications
     */
    public function receiveTasks(Request $request)
    {
        try {
            $tasks = $request->input('tasks', []);
            
            if (empty($tasks)) {
                return response()->json(['error' => 'No tasks provided'], 400);
            }

            foreach ($tasks as $task) {
                $message = $this->formatTaskMessage($task);
                
                // Dispatch job to queue
                SendNotificationJob::dispatch($message);
                
                Log::info('Task notification queued', ['task' => $task]);
            }

            return response()->json([
                'status' => 'success',
                'message' => 'Tasks processed successfully',
                'count' => count($tasks)
            ]);
        } catch (\Exception $e) {
            Log::error('Error processing tasks: ' . $e->getMessage());
            return response()->json(['error' => 'Internal server error'], 500);
        }
    }

    /**
     * Fetch tasks from external API
     */
    public function fetchExternalTasks()
    {
        try {
            $externalApiUrl = config('app.external_api_url');
            
            if (!$externalApiUrl) {
                return response()->json(['error' => 'External API URL not configured'], 400);
            }

            $response = Http::get($externalApiUrl);
            
            if (!$response->successful()) {
                Log::error('Failed to fetch external tasks: ' . $response->body());
                return response()->json(['error' => 'Failed to fetch tasks'], 500);
            }

            $tasks = $response->json();
            
            // Process each task
            foreach ($tasks as $task) {
                $message = $this->formatTaskMessage($task);
                SendNotificationJob::dispatch($message);
            }

            return response()->json([
                'status' => 'success',
                'message' => 'External tasks fetched and processed',
                'count' => count($tasks)
            ]);
        } catch (\Exception $e) {
            Log::error('Error fetching external tasks: ' . $e->getMessage());
            return response()->json(['error' => 'Internal server error'], 500);
        }
    }

    /**
     * Format task data into message
     */
    private function formatTaskMessage(array $task): string
    {
        $title = $task['title'] ?? 'New Task';
        $description = $task['description'] ?? '';
        $priority = $task['priority'] ?? 'normal';
        $dueDate = $task['due_date'] ?? null;

        $message = "<b>🔔 New Task:</b> {$title}\n\n";
        
        if ($description) {
            $message .= "<b>Description:</b> {$description}\n\n";
        }
        
        $message .= "<b>Priority:</b> " . ucfirst($priority) . "\n";
        
        if ($dueDate) {
            $message .= "<b>Due Date:</b> {$dueDate}\n";
        }

        return $message;
    }
}