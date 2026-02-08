# Tasks: Evolution of Todo – Phase V (Advanced Cloud-Native Architecture)

## Feature Overview

This document outlines the implementation tasks for evolving the existing Todo AI Chatbot into a fully event-driven, decoupled, cloud-native system using Kubernetes, Dapr, Kafka (via Dapr Pub/Sub), and multiple independent backend services. The architecture remains stateless, scalable, and resilient.

**Feature**: Cloud-Native Todo System (Phase V)
**Branch**: `001-cloud-native-todo`
**Priority Order**: US1 (P1) → US2 (P1) → US3 (P2) → US4 (P2) → US5 (P3)

## Task Categories

- 🔧 **Setup**: Project initialization and configuration
- 🏗️ **Foundation**: Blocking prerequisites for all user stories
- 📝 **User Story 1**: Create Tasks with Advanced Features
- 🔔 **User Story 2**: Receive Timely Reminders
- 🔄 **User Story 3**: Manage Recurring Tasks
- 🔍 **User Story 4**: Search and Filter Tasks
- ⚡ **User Story 5**: Event-Driven Architecture
- ✨ **Polish**: Cross-cutting concerns and enhancements

---

## Phase 1: Setup Tasks

### Goal
Initialize the project structure and configure the cloud-native infrastructure components.

### Independent Test Criteria
Project structure exists and all required infrastructure components can be deployed.

### Tasks

- [ ] T001 Create project structure per implementation plan in backend/, frontend/, helm/, dapr/
- [ ] T002 Set up shared libraries and utilities in backend/shared/
- [ ] T003 Configure Dapr components directory structure in dapr/components/
- [ ] T004 Create Helm chart structure in helm/todo-chatbot/ and helm/infrastructure/
- [ ] T005 [P] Set up Dockerfiles for all services (chat-api, recurring-task-service, notification-service, audit-service, frontend)

---

## Phase 2: Foundational Tasks

### Goal
Establish the foundational components required by all user stories: database schema, authentication, and basic Dapr integration.

### Independent Test Criteria
Database is accessible, authentication works, and basic Dapr sidecar integration functions.

### Tasks

- [ ] T010 Create PostgreSQL database schema with all required tables and indexes
- [ ] T011 [P] Implement User model in backend/shared/models/user.py
- [ ] T012 [P] Implement Task model in backend/shared/models/task.py
- [ ] T013 [P] Implement Conversation model in backend/shared/models/conversation.py
- [ ] T014 [P] Implement Message model in backend/shared/models/message.py
- [ ] T015 [P] Implement Reminder model in backend/shared/models/reminder.py
- [ ] T016 [P] Implement AuditLog model in backend/shared/models/audit_log.py
- [ ] T017 Set up Dapr pub/sub component configuration for Kafka in dapr/components/pubsub.yaml
- [ ] T018 Set up Dapr state store component configuration for PostgreSQL in dapr/components/statestore.yaml
- [ ] T019 Set up Dapr secrets component configuration in dapr/components/secrets.yaml
- [ ] T020 Set up Dapr jobs component configuration in dapr/components/jobs.yaml
- [ ] T021 Implement authentication middleware using JWT in backend/shared/middleware/auth.py
- [ ] T022 Create database connection utilities in backend/shared/utils/db.py
- [ ] T023 Implement Dapr client wrapper for service invocation in backend/shared/dapr_client/service_invocation.py
- [ ] T024 Implement Dapr client wrapper for pub/sub in backend/shared/dapr_client/pubsub.py
- [ ] T025 Implement Dapr client wrapper for state management in backend/shared/dapr_client/state.py

---

## Phase 3: User Story 1 - Create Tasks with Advanced Features (P1)

### Goal
Enable users to create tasks with due dates, priorities, and tags using natural language through the AI chatbot.

### Independent Test Criteria
Can create tasks with various combinations of due dates, priorities, and tags through the chatbot interface and verify they are properly stored and retrievable.

### Tasks

- [ ] T030 [P] [US1] Create TaskService in backend/chat-api/src/services/task_service.py
- [ ] T031 [P] [US1] Implement create_task_with_advanced_features in TaskService
- [ ] T032 [P] [US1] Create ConversationService in backend/chat-api/src/services/conversation_service.py
- [ ] T033 [P] [US1] Create MessageService in backend/chat-api/src/services/message_service.py
- [ ] T034 [US1] Implement chat endpoint in backend/chat-api/src/api/chat.py
- [ ] T035 [US1] Implement task creation endpoint in backend/chat-api/src/api/tasks.py
- [ ] T036 [US1] Create task parser to extract due dates, priorities, and tags from natural language in backend/chat-api/src/utils/task_parser.py
- [ ] T037 [US1] Implement event publishing for task creation in backend/chat-api/src/services/event_publisher.py
- [ ] T038 [US1] Update frontend to support advanced task creation via chat interface in frontend/src/components/TaskCreation.jsx
- [ ] T039 [US1] Create UI components for displaying task details (due date, priority, tags) in frontend/src/components/TaskDetails.jsx
- [ ] T040 [US1] Implement frontend API client for advanced task features in frontend/src/services/advancedTaskApi.js

---

## Phase 4: User Story 2 - Receive Timely Reminders (P1)

### Goal
Enable asynchronous delivery of reminders at specified times without blocking the main chatbot functionality.

### Independent Test Criteria
Can create tasks with due dates and verify that reminder events are properly scheduled and delivered at the correct time.

### Tasks

- [ ] T050 [P] [US2] Create ReminderService in backend/shared/services/reminder_service.py
- [ ] T051 [US2] Implement schedule_reminder function in ReminderService
- [ ] T052 [US2] Implement process_reminder_event in ReminderService
- [ ] T053 [US2] Create NotificationService in backend/notification-service/src/main.py
- [ ] T054 [US2] Implement reminder event consumer in backend/notification-service/src/consumers/reminder_consumer.py
- [ ] T055 [US2] Implement notification delivery mechanism in backend/notification-service/src/services/notification_service.py
- [ ] T056 [US2] Create Dapr Jobs API integration for scheduling reminders in backend/shared/dapr_client/jobs.py
- [ ] T057 [US2] Update TaskService to trigger reminder scheduling when due dates are set
- [ ] T058 [US2] Implement reminder endpoint in backend/chat-api/src/api/reminders.py
- [ ] T059 [US2] Add reminder functionality to frontend in frontend/src/components/ReminderSettings.jsx

---

## Phase 5: User Story 3 - Manage Recurring Tasks (P2)

### Goal
Allow users to create tasks that repeat automatically, with the system generating next occurrences when completed.

### Independent Test Criteria
Can create recurring tasks, complete them, and verify that the next occurrence is automatically generated.

### Tasks

- [ ] T070 [P] [US3] Create RecurringTaskService in backend/recurring-task-service/src/main.py
- [ ] T071 [US3] Implement recurring task event consumer in backend/recurring-task-service/src/consumers/task_completion_consumer.py
- [ ] T072 [US3] Implement generate_next_occurrence function in backend/recurring-task-service/src/services/recurring_task_service.py
- [ ] T073 [US3] Create cron expression parser for recurring rules in backend/shared/utils/cron_parser.py
- [ ] T074 [US3] Update TaskService to handle recurring task creation
- [ ] T075 [US3] Implement recurring task endpoint in backend/chat-api/src/api/recurring_tasks.py
- [ ] T076 [US3] Add recurring task UI components to frontend in frontend/src/components/RecurringTaskForm.jsx
- [ ] T077 [US3] Update event publisher to handle recurring task events
- [ ] T078 [US3] Create tests for recurring task functionality in backend/recurring-task-service/tests/

---

## Phase 6: User Story 4 - Search and Filter Tasks (P2)

### Goal
Enable users to search and filter their tasks by various criteria like status, priority, tags, or due dates.

### Independent Test Criteria
Can create multiple tasks with different attributes and verify that search and filter functions return the correct results.

### Tasks

- [ ] T090 [P] [US4] Update TaskService with search and filter capabilities in backend/chat-api/src/services/task_service.py
- [ ] T091 [US4] Implement search endpoint in backend/chat-api/src/api/search.py
- [ ] T092 [US4] Implement filter endpoint in backend/chat-api/src/api/tasks.py
- [ ] T093 [US4] Create search utility functions in backend/shared/utils/search_utils.py
- [ ] T094 [US4] Add search and filter functionality to frontend in frontend/src/components/TaskFilters.jsx
- [ ] T095 [US4] Create search results component in frontend/src/components/SearchResults.jsx
- [ ] T096 [US4] Update frontend API client to support search and filter in frontend/src/services/searchApi.js
- [ ] T097 [US4] Optimize database queries for search performance with proper indexing
- [ ] T098 [US4] Implement advanced filtering options (by tags, due dates, etc.)

---

## Phase 7: User Story 5 - Event-Driven Architecture (P3)

### Goal
Implement a robust event-driven architecture that emits events for all task operations and allows other services to consume them.

### Independent Test Criteria
Can perform task operations and verify that corresponding events are emitted and processed by the appropriate services.

### Tasks

- [ ] T110 [P] [US5] Create EventSchema definitions in backend/shared/models/events.py
- [ ] T111 [US5] Implement EventPublisher using Dapr pub/sub in backend/chat-api/src/services/event_publisher.py
- [ ] T112 [US5] Create AuditService in backend/audit-service/src/main.py
- [ ] T113 [US5] Implement audit event consumer in backend/audit-service/src/consumers/audit_consumer.py
- [ ] T114 [US5] Implement audit log storage in backend/audit-service/src/services/audit_service.py
- [ ] T115 [US5] Update all services to properly emit events using Dapr pub/sub
- [ ] T116 [US5] Create event schema documentation in specs/001-cloud-native-todo/event-schemas.md
- [ ] T117 [US5] Implement event validation middleware in backend/shared/middleware/event_validator.py
- [ ] T118 [US5] Create event replay mechanism for recovery in backend/shared/services/event_recovery.py
- [ ] T119 [US5] Add event monitoring and observability features using Dapr tracing

---

## Phase 8: Polish & Cross-Cutting Concerns

### Goal
Address cross-cutting concerns and polish the implementation for production readiness.

### Tasks

- [ ] T130 Create comprehensive error handling middleware in backend/shared/middleware/error_handler.py
- [ ] T131 Implement logging with correlation IDs across all services
- [ ] T132 Add health check endpoints to all services
- [ ] T133 Create integration tests covering all user stories
- [ ] T134 Implement proper configuration management for different environments
- [ ] T135 Add monitoring and metrics collection using Dapr capabilities
- [ ] T136 Create deployment scripts for Minikube and cloud Kubernetes
- [ ] T137 Update Helm charts with proper resource limits and scaling configurations
- [ ] T138 Document the cloud-native architecture and deployment process
- [ ] T139 Perform security review of all Dapr component configurations
- [ ] T140 Conduct performance testing and optimization

---

## Dependencies Between User Stories

1. **US1 (Create Tasks)** → Base functionality needed by all other stories
2. **US2 (Reminders)** → Depends on US1 for task creation with due dates
3. **US3 (Recurring Tasks)** → Depends on US1 for task creation and US5 for event handling
4. **US4 (Search/Filter)** → Depends on US1 for task data
5. **US5 (Event-Driven)** → Underlies all other stories for communication between services

---

## Parallel Execution Opportunities

### Within Each User Story
- Model creation can happen in parallel with service creation
- API endpoints can be developed in parallel with frontend components
- Multiple services can be developed independently after foundational setup

### Across User Stories
- US2 (Reminders) and US3 (Recurring Tasks) can be developed in parallel after US1
- US4 (Search/Filter) can be developed in parallel with US2 and US3
- US5 (Event-Driven) can be implemented incrementally alongside other stories

---

## Implementation Strategy

### MVP Approach
1. Complete Phase 1 (Setup) and Phase 2 (Foundation)
2. Implement US1 (Create Tasks with Advanced Features) as the core functionality
3. Add US5 (Event-Driven Architecture) to connect services
4. Incrementally add US2 (Reminders), US3 (Recurring Tasks), and US4 (Search/Filter)

### Incremental Delivery
- Sprint 1: Setup, Foundation, and basic task creation (US1)
- Sprint 2: Event-driven architecture (US5) and reminders (US2)
- Sprint 3: Recurring tasks (US3) and search/filter (US4)
- Sprint 4: Polish, testing, and deployment

---

## Success Criteria

### Measurable Outcomes
- Users can create tasks with advanced features (due dates, priorities, tags) using natural language in under 30 seconds
- Reminder notifications are delivered within 1 minute of scheduled time for 95% of events
- Recurring tasks are automatically generated correctly for 99% of completed recurring tasks
- Search and filter operations return results in under 2 seconds for collections up to 1000 tasks
- System maintains 99.9% uptime during normal operation with event-driven services functioning
- All task data persists through pod restarts and service redeployments without data loss
- The system supports horizontal scaling with services handling increased load proportionally
- 95% of users can successfully use advanced features (reminders, recurring tasks, priorities) after initial setup
- The cloud-native architecture successfully deploys and runs on both Minikube and managed Kubernetes services