# Research: Evolution of Todo – Phase V (Advanced Cloud-Native Architecture)

## Overview
This document captures the research conducted to support the evolution of the Todo AI Chatbot into a fully event-driven, decoupled, cloud-native system using Kubernetes, Dapr, Kafka (via Dapr Pub/Sub), and multiple independent backend services.

## Decision: Dapr as the Infrastructure Abstraction Layer
**Rationale:** Using Dapr (Distributed Application Runtime) provides a consistent set of APIs for common distributed system challenges without tightly coupling the application code to specific infrastructure implementations. This allows the application to remain portable across different environments while abstracting away the complexity of connecting to various infrastructure components.

**Alternatives considered:**
- Direct Kafka client integration: Would create tight coupling and violate the constitution's requirement that Kafka only be accessed via Dapr
- Manual service discovery: Would increase complexity and violate the requirement to avoid hardcoded service URLs
- Traditional microservice frameworks: Would not provide the same level of infrastructure abstraction as Dapr

## Decision: Event-Driven Architecture with Kafka via Dapr Pub/Sub
**Rationale:** An event-driven architecture enables loose coupling between services, allowing them to evolve independently and scale separately. Using Kafka through Dapr's pub/sub building block ensures compliance with the constitution while providing reliable, scalable messaging between services.

**Alternatives considered:**
- Synchronous REST APIs between services: Would create tight coupling and violate the event-driven first principle
- Message queues like RabbitMQ: Would require direct integration, violating the requirement to use Kafka only via Dapr
- Database polling: Would be inefficient and not meet scalability requirements

## Decision: Multiple Independent Backend Services
**Rationale:** Breaking the system into multiple independent services allows each to be developed, deployed, and scaled independently. This supports the cloud-native architecture goals and enables teams to work on different services without interference.

**Services identified:**
- Frontend Service: Next.js UI that forwards messages to Chat API via Dapr service invocation
- Chat API Service: FastAPI service for conversation orchestration and natural language understanding
- Recurring Task Service: Listens for task.completed events and generates next instance for recurring tasks
- Notification Service: Consumes reminder events and delivers notifications
- Audit Service: Persists immutable task activity history

**Alternatives considered:**
- Monolithic architecture: Would not support the decoupling requirements
- Fewer services: Would not allow for independent scaling of specific responsibilities

## Decision: Kubernetes for Orchestration
**Rationale:** Kubernetes provides industry-standard orchestration for containerized applications, supporting the required scalability, resilience, and portability. It integrates well with Dapr and supports the cloud-native architecture goals.

**Alternatives considered:**
- Docker Swarm: Less feature-rich than Kubernetes
- Cloud-specific orchestration (AWS ECS, Azure Container Instances): Would limit portability
- Serverless platforms: Would not provide the required control over service interactions

## Decision: Helm for Deployment
**Rationale:** Helm provides templated, versioned, and configurable deployments that are essential for managing complex Kubernetes applications. It supports the requirement for environment-specific configurations and automated deployments.

**Alternatives considered:**
- Raw Kubernetes manifests: Would require manual management of environment differences
- Kustomize: Would not provide the same level of parameterization as Helm
- Terraform: More suited for infrastructure provisioning than application deployment

## Decision: Minikube for Local Development
**Rationale:** Minikube provides a local Kubernetes environment that closely mirrors production while being lightweight enough for development. This supports the requirement for a consistent environment across development and production.

**Alternatives considered:**
- Docker Compose: Would not provide the same Kubernetes experience for development
- Kind (Kubernetes in Docker): Would work but Minikube is more established for local development
- Remote development clusters: Would add complexity and network dependencies

## Decision: CI/CD with GitHub Actions
**Rationale:** GitHub Actions provides seamless integration with the repository while supporting the required build, test, and deployment workflows. It can automate Docker image building and Helm-based deployments.

**Alternatives considered:**
- Jenkins: Would require additional infrastructure
- GitLab CI/CD: Not applicable since using GitHub
- Cloud-specific CI/CD: Would tie to specific cloud providers

## Technology Deep Dive: Dapr Building Blocks

### Dapr Pub/Sub
- **Purpose:** Enable event-driven architectures with publish-subscribe messaging
- **Implementation:** Use Dapr's pub/sub building block to publish task lifecycle events
- **Topics planned:**
  - task-events: Task lifecycle changes (created, updated, completed, deleted)
  - reminders: Scheduled reminder notifications
  - task-updates: Optional real-time sync events

### Dapr State Store
- **Purpose:** Store and retrieve state with resiliency features
- **Implementation:** Use PostgreSQL as state store via Dapr component
- **Use cases:**
  - Conversation context persistence
  - Temporary task-related state
  - User session data

### Dapr Service Invocation
- **Purpose:** Enable service-to-service communication with service discovery
- **Implementation:** Use Dapr's service invocation API for communication between services
- **Use cases:**
  - Frontend → Chat API calls
  - Internal service communication (when needed)

### Dapr Secret Store
- **Purpose:** Securely store and access sensitive information
- **Implementation:** Use Kubernetes secrets via Dapr component
- **Use cases:**
  - Database credentials
  - API keys
  - TLS certificates

### Dapr Jobs API
- **Purpose:** Schedule and manage job execution
- **Implementation:** Use Dapr's Jobs API for exact-time reminders and recurring task scheduling
- **Use cases:**
  - Exact-time reminder notifications
  - Recurring task scheduling
  - Periodic cleanup tasks

## Architecture Patterns Researched

### Event Sourcing
- **Description:** Store state as a sequence of events rather than current state snapshots
- **Consideration:** Not fully adopted due to complexity but event-driven approach is used
- **Benefits:** Complete audit trail, temporal queries, replay capabilities
- **Trade-offs:** Increased complexity, storage overhead

### CQRS (Command Query Responsibility Segregation)
- **Description:** Separate read and write models to optimize for different concerns
- **Consideration:** Partially adopted in the service design (different services for different responsibilities)
- **Benefits:** Optimized read/write performance, scalability
- **Trade-offs:** Increased complexity, eventual consistency challenges

### Saga Pattern
- **Description:** Manage distributed transactions across services
- **Consideration:** Relevant for complex operations spanning multiple services
- **Benefits:** Maintain consistency across services
- **Trade-offs:** Complexity in implementation and debugging

## Security Considerations

### Service-to-Service Authentication
- **Approach:** Use Dapr's mTLS for service-to-service communication
- **Implementation:** Enable Dapr's built-in mutual TLS for all service communications

### API Security
- **Approach:** JWT tokens for user authentication, Dapr for service authentication
- **Implementation:** Maintain existing JWT-based user authentication while using Dapr for service identity

### Data Encryption
- **Approach:** Encrypt data in transit and at rest
- **Implementation:** TLS for all communications, encrypted storage in PostgreSQL

## Scalability Strategies Researched

### Horizontal Pod Autoscaling (HPA)
- **Implementation:** Configure HPA for all services based on CPU and memory metrics
- **Benefits:** Automatically adjust replica count based on demand

### Event Consumer Scaling
- **Implementation:** Kafka consumers scale independently based on topic partition count
- **Benefits:** Independent scaling of event processing services

### Database Connection Management
- **Implementation:** Connection pooling and proper resource management
- **Benefits:** Efficient resource utilization under varying loads

## Monitoring and Observability

### Distributed Tracing
- **Implementation:** Use Dapr's built-in tracing capabilities with Zipkin/Jaeger
- **Benefits:** Track requests across service boundaries

### Metrics Collection
- **Implementation:** Prometheus metrics exported by Dapr sidecars
- **Benefits:** Monitor service health and performance

### Logging
- **Implementation:** Structured logging with correlation IDs
- **Benefits:** Debug and troubleshoot distributed systems effectively

## Conclusion
The research confirms that the proposed architecture using Kubernetes, Dapr, Kafka (via Dapr Pub/Sub), and multiple independent backend services is technically feasible and aligns with the project's requirements for a cloud-native, event-driven system. The architecture supports the required scalability, resilience, and maintainability goals while complying with the constitutional requirements.