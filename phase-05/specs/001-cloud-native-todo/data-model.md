# Data Model: Evolution of Todo – Phase V (Advanced Cloud-Native Architecture)

## Overview
This document defines the data models for the cloud-native todo system, focusing on the entities that will be persisted in the PostgreSQL database and the event structures used for communication between services via Kafka through Dapr Pub/Sub.

## Core Entities

### 1. User
Represents a registered user of the system.

```sql
CREATE TABLE "user" (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  is_active BOOLEAN NOT NULL DEFAULT true,
  last_login_at TIMESTAMP WITH TIME ZONE
);
```

**Fields:**
- `id`: Unique identifier for the user (UUID)
- `email`: User's email address (unique)
- `password_hash`: BCrypt hash of the user's password
- `created_at`: Timestamp when the user was created
- `updated_at`: Timestamp when the user record was last updated
- `is_active`: Flag indicating if the user account is active
- `last_login_at`: Timestamp of the user's last login

**Validation Rules:**
- Email must be a valid email format
- Password hash must not be empty
- Email must be unique across all users

### 2. Task
Represents a task in the todo system.

```sql
CREATE TABLE task (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  completed BOOLEAN NOT NULL DEFAULT false,
  priority INTEGER NOT NULL DEFAULT 0 CHECK (priority >= 0 AND priority <= 2), -- 0: low, 1: medium, 2: high
  due_date TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  completed_at TIMESTAMP WITH TIME ZONE,
  recurring_rule VARCHAR(255), -- Cron expression for recurring tasks
  parent_task_id UUID REFERENCES task(id) ON DELETE SET NULL -- For recurring task instances
);
```

**Fields:**
- `id`: Unique identifier for the task (UUID)
- `user_id`: Reference to the user who owns the task
- `title`: Title of the task (required)
- `description`: Optional description of the task
- `completed`: Boolean indicating if the task is completed
- `priority`: Priority level (0: low, 1: medium, 2: high)
- `due_date`: Optional due date for the task
- `created_at`: Timestamp when the task was created
- `updated_at`: Timestamp when the task was last updated
- `completed_at`: Timestamp when the task was marked as completed
- `recurring_rule`: Cron expression for recurring tasks
- `parent_task_id`: Reference to the parent task for recurring task instances

**Validation Rules:**
- Title must not be empty
- Priority must be between 0 and 2
- Due date must be in the future if provided
- Parent task ID must refer to a valid task if provided

### 3. Conversation
Represents a conversation between the user and the AI assistant.

```sql
CREATE TABLE conversation (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  is_active BOOLEAN NOT NULL DEFAULT true
);
```

**Fields:**
- `id`: Unique identifier for the conversation (UUID)
- `user_id`: Reference to the user who owns the conversation
- `title`: Title of the conversation (auto-generated from first message)
- `created_at`: Timestamp when the conversation was created
- `updated_at`: Timestamp when the conversation was last updated
- `is_active`: Flag indicating if the conversation is active

**Validation Rules:**
- Title must not be empty
- User ID must refer to a valid user

### 4. Message
Represents a message in a conversation.

```sql
CREATE TABLE message (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES conversation(id) ON DELETE CASCADE,
  role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  content TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  metadata JSONB -- Additional metadata for the message
);
```

**Fields:**
- `id`: Unique identifier for the message (UUID)
- `conversation_id`: Reference to the conversation this message belongs to
- `role`: Role of the message sender ('user', 'assistant', 'system')
- `content`: Content of the message
- `created_at`: Timestamp when the message was created
- `updated_at`: Timestamp when the message was last updated
- `metadata`: Additional metadata for the message (JSONB)

**Validation Rules:**
- Role must be one of 'user', 'assistant', or 'system'
- Content must not be empty
- Conversation ID must refer to a valid conversation

### 5. Reminder
Represents a scheduled reminder for a task.

```sql
CREATE TABLE reminder (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID NOT NULL REFERENCES task(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  scheduled_at TIMESTAMP WITH TIME ZONE NOT NULL,
  sent_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  is_active BOOLEAN NOT NULL DEFAULT true
);
```

**Fields:**
- `id`: Unique identifier for the reminder (UUID)
- `task_id`: Reference to the task this reminder is for
- `user_id`: Reference to the user who owns the reminder
- `scheduled_at`: Timestamp when the reminder should be sent
- `sent_at`: Timestamp when the reminder was actually sent
- `created_at`: Timestamp when the reminder was created
- `updated_at`: Timestamp when the reminder was last updated
- `is_active`: Flag indicating if the reminder is still active

**Validation Rules:**
- Scheduled time must be in the future
- Task ID must refer to a valid task
- User ID must refer to a valid user

### 6. Audit Log
Represents an immutable log of task activities for the audit service.

```sql
CREATE TABLE audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID NOT NULL,
  user_id UUID NOT NULL,
  action VARCHAR(50) NOT NULL CHECK (action IN ('created', 'updated', 'completed', 'deleted', 'recurring_created')),
  previous_state JSONB, -- Previous state of the task before the action
  new_state JSONB, -- New state of the task after the action
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  metadata JSONB -- Additional metadata about the action
);
```

**Fields:**
- `id`: Unique identifier for the audit log entry (UUID)
- `task_id`: Reference to the task this audit log is for (stored as UUID to maintain immutability even if task is deleted)
- `user_id`: Reference to the user who performed the action (stored as UUID to maintain immutability)
- `action`: Type of action performed ('created', 'updated', 'completed', 'deleted', 'recurring_created')
- `previous_state`: JSON representation of the task state before the action
- `new_state`: JSON representation of the task state after the action
- `created_at`: Timestamp when the audit log entry was created
- `metadata`: Additional metadata about the action (JSONB)

**Validation Rules:**
- Action must be one of the allowed values
- Previous state and new state must be valid JSON representations of a task

## Event Schema

### 1. TaskEvent
Generic event structure for all task-related events.

```json
{
  "id": "uuid",
  "timestamp": "ISO 8601 timestamp",
  "eventType": "task.created | task.updated | task.completed | task.deleted | task.recurring_created",
  "userId": "uuid",
  "taskId": "uuid",
  "payload": {
    // Specific payload depending on eventType
  },
  "correlationId": "uuid",
  "causationId": "uuid"
}
```

### 2. TaskCreatedEvent
Published when a new task is created.

```json
{
  "id": "uuid",
  "timestamp": "ISO 8601 timestamp",
  "eventType": "task.created",
  "userId": "uuid",
  "taskId": "uuid",
  "payload": {
    "task": {
      "id": "uuid",
      "userId": "uuid",
      "title": "string",
      "description": "string",
      "completed": false,
      "priority": 1,
      "dueDate": "ISO 8601 timestamp",
      "createdAt": "ISO 8601 timestamp",
      "updatedAt": "ISO 8601 timestamp",
      "completedAt": null,
      "recurringRule": null,
      "parentTaskId": null
    }
  },
  "correlationId": "uuid",
  "causationId": "uuid"
}
```

### 3. TaskUpdatedEvent
Published when a task is updated.

```json
{
  "id": "uuid",
  "timestamp": "ISO 8601 timestamp",
  "eventType": "task.updated",
  "userId": "uuid",
  "taskId": "uuid",
  "payload": {
    "task": {
      "id": "uuid",
      "userId": "uuid",
      "title": "string",
      "description": "string",
      "completed": false,
      "priority": 1,
      "dueDate": "ISO 8601 timestamp",
      "createdAt": "ISO 8601 timestamp",
      "updatedAt": "ISO 8601 timestamp",
      "completedAt": null,
      "recurringRule": null,
      "parentTaskId": null
    },
    "changes": {
      "field": "old_value -> new_value"
    }
  },
  "correlationId": "uuid",
  "causationId": "uuid"
}
```

### 4. TaskCompletedEvent
Published when a task is marked as completed.

```json
{
  "id": "uuid",
  "timestamp": "ISO 8601 timestamp",
  "eventType": "task.completed",
  "userId": "uuid",
  "taskId": "uuid",
  "payload": {
    "task": {
      "id": "uuid",
      "userId": "uuid",
      "title": "string",
      "description": "string",
      "completed": true,
      "priority": 1,
      "dueDate": "ISO 8601 timestamp",
      "createdAt": "ISO 8601 timestamp",
      "updatedAt": "ISO 8601 timestamp",
      "completedAt": "ISO 8601 timestamp",
      "recurringRule": null,
      "parentTaskId": null
    }
  },
  "correlationId": "uuid",
  "causationId": "uuid"
}
```

### 5. TaskDeletedEvent
Published when a task is deleted.

```json
{
  "id": "uuid",
  "timestamp": "ISO 8601 timestamp",
  "eventType": "task.deleted",
  "userId": "uuid",
  "taskId": "uuid",
  "payload": {
    "taskId": "uuid"
  },
  "correlationId": "uuid",
  "causationId": "uuid"
}
```

### 6. RecurringTaskCreatedEvent
Published when a recurring task instance is created.

```json
{
  "id": "uuid",
  "timestamp": "ISO 8601 timestamp",
  "eventType": "task.recurring_created",
  "userId": "uuid",
  "taskId": "uuid",
  "payload": {
    "task": {
      "id": "uuid",
      "userId": "uuid",
      "title": "string",
      "description": "string",
      "completed": false,
      "priority": 1,
      "dueDate": "ISO 8601 timestamp",
      "createdAt": "ISO 8601 timestamp",
      "updatedAt": "ISO 8601 timestamp",
      "completedAt": null,
      "recurringRule": "cron_expression",
      "parentTaskId": "uuid" // References the original recurring task
    },
    "parentTaskId": "uuid"
  },
  "correlationId": "uuid",
  "causationId": "uuid"
}
```

### 7. ReminderEvent
Published when a reminder should be sent.

```json
{
  "id": "uuid",
  "timestamp": "ISO 8601 timestamp",
  "eventType": "reminder.triggered",
  "userId": "uuid",
  "taskId": "uuid",
  "payload": {
    "reminderId": "uuid",
    "task": {
      "id": "uuid",
      "userId": "uuid",
      "title": "string",
      "description": "string",
      "completed": false,
      "priority": 1,
      "dueDate": "ISO 8601 timestamp",
      "createdAt": "ISO 8601 timestamp",
      "updatedAt": "ISO 8601 timestamp",
      "completedAt": null,
      "recurringRule": null,
      "parentTaskId": null
    }
  },
  "correlationId": "uuid",
  "causationId": "uuid"
}
```

## Indexes

### 1. User Table Indexes
```sql
-- Index on email for fast login lookups
CREATE INDEX idx_user_email ON "user"(email);

-- Index on active status for filtering
CREATE INDEX idx_user_is_active ON "user"(is_active);

-- Index on last login for analytics
CREATE INDEX idx_user_last_login ON "user"(last_login_at);
```

### 2. Task Table Indexes
```sql
-- Index on user_id for filtering tasks by user
CREATE INDEX idx_task_user_id ON task(user_id);

-- Index on completed status for filtering
CREATE INDEX idx_task_completed ON task(completed);

-- Index on due date for reminder scheduling
CREATE INDEX idx_task_due_date ON task(due_date) WHERE due_date IS NOT NULL;

-- Index on priority for sorting
CREATE INDEX idx_task_priority ON task(priority);

-- Index on parent_task_id for recurring tasks
CREATE INDEX idx_task_parent_task_id ON task(parent_task_id);

-- Composite index for common queries
CREATE INDEX idx_task_user_completed_priority ON task(user_id, completed, priority);
```

### 3. Conversation Table Indexes
```sql
-- Index on user_id for filtering conversations by user
CREATE INDEX idx_conversation_user_id ON conversation(user_id);

-- Index on active status for filtering
CREATE INDEX idx_conversation_is_active ON conversation(is_active);

-- Index on updated_at for ordering by recency
CREATE INDEX idx_conversation_updated_at ON conversation(updated_at);
```

### 4. Message Table Indexes
```sql
-- Index on conversation_id for filtering messages by conversation
CREATE INDEX idx_message_conversation_id ON message(conversation_id);

-- Index on role for filtering messages by sender type
CREATE INDEX idx_message_role ON message(role);

-- Index on created_at for ordering messages chronologically
CREATE INDEX idx_message_created_at ON message(created_at);
```

### 5. Reminder Table Indexes
```sql
-- Index on task_id for filtering reminders by task
CREATE INDEX idx_reminder_task_id ON reminder(task_id);

-- Index on user_id for filtering reminders by user
CREATE INDEX idx_reminder_user_id ON reminder(user_id);

-- Index on scheduled_at for scheduling system
CREATE INDEX idx_reminder_scheduled_at ON reminder(scheduled_at) WHERE is_active = true;

-- Index on sent_at for tracking sent reminders
CREATE INDEX idx_reminder_sent_at ON reminder(sent_at) WHERE sent_at IS NOT NULL;
```

### 6. Audit Log Table Indexes
```sql
-- Index on task_id for filtering audit logs by task
CREATE INDEX idx_audit_log_task_id ON audit_log(task_id);

-- Index on user_id for filtering audit logs by user
CREATE INDEX idx_audit_log_user_id ON audit_log(user_id);

-- Index on action type for filtering audit logs by action
CREATE INDEX idx_audit_log_action ON audit_log(action);

-- Index on created_at for chronological ordering
CREATE INDEX idx_audit_log_created_at ON audit_log(created_at);

-- Composite index for common audit queries
CREATE INDEX idx_audit_log_task_action_time ON audit_log(task_id, action, created_at);
```

## State Transitions

### Task State Transitions
1. **Created** → **Active**: When a task is first created
2. **Active** → **Completed**: When a task is marked as completed
3. **Completed** → **Active**: When a completed task is marked as incomplete
4. **Any State** → **Deleted**: When a task is deleted

### Reminder State Transitions
1. **Scheduled** → **Sent**: When a reminder is triggered and sent
2. **Scheduled** → **Cancelled**: When a reminder is cancelled (e.g., if the task is deleted)

## Relationships

### User ↔ Task
- One-to-Many: One user can have many tasks
- Referenced by: `task.user_id` → `user.id`
- Cascade delete: When a user is deleted, all their tasks are also deleted

### Task ↔ Reminder
- One-to-Many: One task can have many reminders
- Referenced by: `reminder.task_id` → `task.id`
- Cascade delete: When a task is deleted, all its reminders are also deleted

### User ↔ Reminder
- One-to-Many: One user can have many reminders
- Referenced by: `reminder.user_id` → `user.id`
- Cascade delete: When a user is deleted, all their reminders are also deleted

### Conversation ↔ Message
- One-to-Many: One conversation can have many messages
- Referenced by: `message.conversation_id` → `conversation.id`
- Cascade delete: When a conversation is deleted, all its messages are also deleted

### Task ↔ Audit Log
- One-to-Many: One task can have many audit log entries
- Referenced by: `audit_log.task_id` → `task.id` (stored as UUID to maintain immutability)
- No cascade delete: Audit logs remain even if the task is deleted