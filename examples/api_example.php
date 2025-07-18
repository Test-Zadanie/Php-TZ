<?php

/**
 * Example of external API integration
 * Demonstrates how to send tasks to the notification service
 */

// Example 1: Send tasks to notification service
function sendTasksToNotificationService($tasks) {
    $apiUrl = 'https://yourapp.com/api/v1/tasks';
    
    $data = json_encode(['tasks' => $tasks]);
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $apiUrl);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Content-Length: ' . strlen($data)
    ]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode === 200) {
        echo "Tasks sent successfully!\n";
        echo "Response: " . $response . "\n";
    } else {
        echo "Error sending tasks. HTTP Code: " . $httpCode . "\n";
    }
}

// Example tasks data
$tasks = [
    [
        'title' => 'Deploy new version',
        'description' => 'Deploy version 2.1.0 to production server',
        'priority' => 'high',
        'due_date' => '2024-01-15'
    ],
    [
        'title' => 'Database backup',
        'description' => 'Create backup of production database',
        'priority' => 'medium',
        'due_date' => '2024-01-10'
    ],
    [
        'title' => 'Code review',
        'description' => 'Review pull request #123',
        'priority' => 'normal',
        'due_date' => null
    ]
];

// Send tasks
sendTasksToNotificationService($tasks);

// Example 2: Fetch tasks from external API
function fetchExternalTasks() {
    $apiUrl = 'https://yourapp.com/api/v1/tasks/fetch';
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $apiUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode === 200) {
        echo "External tasks fetched successfully!\n";
        echo "Response: " . $response . "\n";
    } else {
        echo "Error fetching external tasks. HTTP Code: " . $httpCode . "\n";
    }
}

// Fetch external tasks
fetchExternalTasks();