-- Database schema for Evolution of Todo – Phase V (Advanced Cloud-Native Architecture)
-- Creates all required tables and indexes for the PostgreSQL database

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. User table
CREATE TABLE IF NOT EXISTS "user" (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  is_active BOOLEAN NOT NULL DEFAULT true,
  last_login_at TIMESTAMP WITH TIME ZONE
);

-- 2. Conversation table
CREATE TABLE IF NOT EXISTS conversation (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  is_active BOOLEAN NOT NULL DEFAULT true
);

-- 3. Message table
CREATE TABLE IF NOT EXISTS message (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  conversation_id UUID NOT NULL REFERENCES conversation(id) ON DELETE CASCADE,
  role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  content TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  metadata JSONB
);

-- 4. Task table
CREATE TABLE IF NOT EXISTS task (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
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

-- 5. Reminder table
CREATE TABLE IF NOT EXISTS reminder (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  task_id UUID NOT NULL REFERENCES task(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  scheduled_at TIMESTAMP WITH TIME ZONE NOT NULL,
  sent_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  is_active BOOLEAN NOT NULL DEFAULT true
);

-- 6. Audit Log table
CREATE TABLE IF NOT EXISTS audit_log (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  task_id UUID NOT NULL,
  user_id UUID NOT NULL,
  action VARCHAR(50) NOT NULL CHECK (action IN ('created', 'updated', 'completed', 'deleted', 'recurring_created')),
  previous_state JSONB, -- Previous state of the task before the action
  new_state JSONB, -- New state of the task after the action
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  metadata JSONB -- Additional metadata about the action
);

-- Indexes

-- 1. User Table Indexes
CREATE INDEX IF NOT EXISTS idx_user_email ON "user"(email);
CREATE INDEX IF NOT EXISTS idx_user_is_active ON "user"(is_active);
CREATE INDEX IF NOT EXISTS idx_user_last_login ON "user"(last_login_at);

-- 2. Task Table Indexes
CREATE INDEX IF NOT EXISTS idx_task_user_id ON task(user_id);
CREATE INDEX IF NOT EXISTS idx_task_completed ON task(completed);
CREATE INDEX IF NOT EXISTS idx_task_due_date ON task(due_date) WHERE due_date IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_task_priority ON task(priority);
CREATE INDEX IF NOT EXISTS idx_task_parent_task_id ON task(parent_task_id);
CREATE INDEX IF NOT EXISTS idx_task_user_completed_priority ON task(user_id, completed, priority);

-- 3. Conversation Table Indexes
CREATE INDEX IF NOT EXISTS idx_conversation_user_id ON conversation(user_id);
CREATE INDEX IF NOT EXISTS idx_conversation_is_active ON conversation(is_active);
CREATE INDEX IF NOT EXISTS idx_conversation_updated_at ON conversation(updated_at);

-- 4. Message Table Indexes
CREATE INDEX IF NOT EXISTS idx_message_conversation_id ON message(conversation_id);
CREATE INDEX IF NOT EXISTS idx_message_role ON message(role);
CREATE INDEX IF NOT EXISTS idx_message_created_at ON message(created_at);

-- 5. Reminder Table Indexes
CREATE INDEX IF NOT EXISTS idx_reminder_task_id ON reminder(task_id);
CREATE INDEX IF NOT EXISTS idx_reminder_user_id ON reminder(user_id);
CREATE INDEX IF NOT EXISTS idx_reminder_scheduled_at ON reminder(scheduled_at) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_reminder_sent_at ON reminder(sent_at) WHERE sent_at IS NOT NULL;

-- 6. Audit Log Table Indexes
CREATE INDEX IF NOT EXISTS idx_audit_log_task_id ON audit_log(task_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_action ON audit_log(action);
CREATE INDEX IF NOT EXISTS idx_audit_log_created_at ON audit_log(created_at);
CREATE INDEX IF NOT EXISTS idx_audit_log_task_action_time ON audit_log(task_id, action, created_at);