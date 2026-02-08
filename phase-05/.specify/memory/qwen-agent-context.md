# Qwen Code Agent Context: Evolution of Todo – Phase V (Advanced Cloud-Native Architecture)

## Overview
This file contains context for the Qwen Code agent to work effectively on the Evolution of Todo – Phase V project, which transforms the existing Todo AI Chatbot into a fully event-driven, decoupled, cloud-native system using Kubernetes, Dapr, Kafka (via Dapr Pub/Sub), and multiple independent backend services.

## Architecture Context

### System Components
The system consists of the following runtime layers:
1. User Interface Layer (Next.js frontend)
2. Conversational AI Layer (Chat API Service)
3. Event-Driven Domain Services (Recurring Task, Notification, Audit)
4. Infrastructure Abstraction Layer (Dapr)
5. Messaging Layer (Kafka via Dapr Pub/Sub)
6. Persistence Layer (Neon PostgreSQL)

### Core Services
1. **Frontend Service**: Next.js + OpenAI ChatKit for chat UI
2. **Chat API Service**: FastAPI + OpenAI Agents SDK + MCP for conversation orchestration
3. **Recurring Task Service**: Generates next instances for recurring tasks
4. **Notification Service**: Delivers reminder notifications
5. **Audit Service**: Persists immutable task activity history

## Technology Stack

### Infrastructure & Orchestration
- **Kubernetes**: Container orchestration (Minikube for local, AKS/GKE/OKE for cloud)
- **Helm**: Package manager for Kubernetes deployments
- **Docker**: Containerization of all services

### Service Mesh & Middleware
- **Dapr (Distributed Application Runtime)**: Infrastructure abstraction layer
  - Dapr Pub/Sub: Event-driven communication via Kafka
  - Dapr State Store: State management backed by PostgreSQL
  - Dapr Service Invocation: Service-to-service communication
  - Dapr Secrets: Secure credential management
  - Dapr Jobs API: Task scheduling

### Messaging
- **Apache Kafka**: Event streaming platform (accessed only via Dapr Pub/Sub)
- **Kafka Topics**:
  - `task-events`: Task lifecycle changes
  - `reminders`: Scheduled reminder notifications
  - `task-updates`: Optional real-time sync events

### Persistence
- **PostgreSQL**: Primary data store (Neon for cloud, local instance for dev)
- **Event Store**: Kafka topics serve as immutable event log

### Languages & Frameworks
- **Backend**: Python 3.11, FastAPI
- **Frontend**: TypeScript/JavaScript, Next.js
- **API Clients**: Generated from OpenAPI specs

## Event Architecture

### Event Flow
1. Chat API publishes task lifecycle events via Dapr Pub/Sub
2. Kafka topics receive events through Dapr
3. Domain services consume events independently
4. No service depends on another synchronously

### Event Schema
Events follow a consistent structure with id, timestamp, eventType, userId, taskId, payload, correlationId, and causationId.

## Dapr Integration

### Components Used
- **Pub/Sub**: Kafka via Dapr component configuration
- **State Store**: PostgreSQL via Dapr component configuration
- **Secrets**: Kubernetes secrets via Dapr
- **Service Invocation**: For frontend → Chat API calls

### Configuration
Dapr components are defined in YAML files under the `dapr/components/` directory.

## Deployment Architecture

### Local Development
- **Platform**: Minikube or Docker Desktop Kubernetes
- **Services**: Deployed via Helm charts
- **Dapr**: Sidecars injected automatically

### Cloud Deployment
- **Platforms**: AKS, GKE, or OKE
- **Strategy**: Same Helm charts with environment-specific values
- **CI/CD**: GitHub Actions with Helm-based deployments

## Development Guidelines

### Coding Standards
1. **No Direct Infrastructure Access**: All infrastructure access must go through Dapr building blocks
2. **Event-Driven First**: Prefer event-driven communication over synchronous calls
3. **Stateless Services**: All services must be stateless and horizontally scalable
4. **Immutable Events**: Events once published should never be modified

### Security
1. **No Hardcoded Credentials**: Use Dapr Secrets or Kubernetes Secrets
2. **No Hardcoded URLs**: Use Dapr Service Invocation for inter-service communication
3. **JWT Authentication**: Maintain existing JWT-based user authentication

### Testing
1. **Event Replay Safety**: Ensure all consumers are idempotent
2. **At-Least-Once Delivery**: Design for potential duplicate events
3. **Service Independence**: Test services in isolation

## Key Directories and Files

### Specifications
- `specs/001-cloud-native-todo/`: Main specification directory
- `specs/001-cloud-native-todo/data-model.md`: Data models and event schemas
- `specs/001-cloud-native-todo/research.md`: Research and technology decisions
- `specs/001-cloud-native-todo/quickstart.md`: Setup and deployment guide
- `specs/001-cloud-native-todo/contracts/`: API contracts (OpenAPI specs)

### Infrastructure
- `dapr/components/`: Dapr component configurations
- `helm/todo-chatbot/`: Main application Helm chart
- `helm/infrastructure/`: Infrastructure Helm chart

### Services
- `backend/chat-api/`: Chat API service
- `backend/recurring-task-service/`: Recurring task service
- `backend/notification-service/`: Notification service
- `backend/audit-service/`: Audit service
- `frontend/`: Next.js frontend application

## Important Notes for Implementation

1. **Constitution Compliance**: All changes must comply with the project constitution
2. **Spec-Driven Development**: Follow the speckit.specify → speckit.plan → speckit.tasks workflow
3. **Dapr First**: Always use Dapr building blocks for infrastructure access
4. **Event-Driven Architecture**: Design with loose coupling and independent scaling in mind
5. **Cloud-Native Principles**: Embrace statelessness, horizontal scalability, and resilience

## Common Commands

### Local Development
```bash
# Start Minikube
minikube start --memory=8192 --cpus=4

# Install Dapr
dapr init -k

# Deploy infrastructure
helm install postgresql bitnami/postgresql --namespace postgresql --create-namespace
helm install strimzi strimzi/strimzi-kafka-operator --namespace kafka --create-namespace

# Deploy application
helm install todo-chatbot ./helm/todo-chatbot --namespace todo-chatbot --create-namespace

# Port forward to access frontend
kubectl port-forward svc/frontend 3000:80 -n todo-chatbot
```

### Verification
```bash
# Check all pods
kubectl get pods -n todo-chatbot

# Check Dapr sidecars
dapr list -k

# Check Dapr logs
kubectl logs -l app=chat-api -n todo-chatbot -c daprd
```