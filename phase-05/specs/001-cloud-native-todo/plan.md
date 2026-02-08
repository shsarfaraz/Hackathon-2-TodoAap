# Implementation Plan: Evolution of Todo – Phase V (Advanced Cloud-Native Architecture)

**Branch**: `001-cloud-native-todo` | **Date**: 2026-02-07 | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Evolution of the existing Todo AI Chatbot into a fully event-driven, decoupled, cloud-native system using Kubernetes, Dapr, Kafka (via Dapr Pub/Sub), and multiple independent backend services. The architecture must remain stateless, scalable, and resilient.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/JavaScript (Node.js 20+), Helm v3
**Primary Dependencies**: FastAPI, Next.js, Dapr, Kafka, PostgreSQL (Neon), Kubernetes, Helm
**Storage**: PostgreSQL (Neon) for primary data, Kafka for event streaming, Redis for caching
**Testing**: pytest, Jest, integration tests for event flows
**Target Platform**: Kubernetes (Minikube for local, AKS/GKE/OKE for cloud)
**Project Type**: Distributed microservices with web frontend
**Performance Goals**: Event-driven processing with <100ms latency, horizontal scalability to 10k concurrent users
**Constraints**: Must use Dapr for infrastructure abstraction, Kafka only via Dapr Pub/Sub, no hardcoded service URLs
**Scale/Scope**: Event-driven architecture supporting millions of tasks, horizontal pod autoscaling

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the constitution file, the following requirements must be met:

### Spec-Driven Only
- [X] All changes follow spec-driven development (speckit.specify → speckit.plan → speckit.tasks)
- [X] No code, config, or infrastructure changes without proper documentation

### Cloud-Native Architecture
- [X] All services are stateless
- [X] All services are horizontally scalable
- [X] All services are Kubernetes-native
- [X] Communication prefers event-driven (Kafka via Dapr) and service invocation via Dapr

### Event-Driven First (Kafka + Dapr)
- [X] All task lifecycle events emit domain events (created, updated, completed, deleted)
- [X] Kafka accessed ONLY through Dapr
- [X] Dapr Pub/Sub is the ONLY allowed interface for events

### Advanced Features via Decoupled Services
- [X] Recurring Task Engine implemented as separate service
- [X] Reminder/Notification Service implemented as separate service
- [X] Audit/Activity Log Service implemented as separate service
- [X] Each service performs single responsibility and can be independently scaled

### Dapr as the Infrastructure Abstraction Layer
- [X] Application code does NOT import Kafka clients
- [X] Application code does NOT embed database credentials
- [X] Application code does NOT hardcode service URLs
- [X] Applications use Dapr Pub/Sub, State Store, Jobs API, Service Invocation, and Secrets

### Docker & Containers
- [X] All services run as containers
- [X] Dockerfiles generated via Claude Code
- [X] Local runtime: Minikube
- [X] Cloud runtime: AKS / GKE / OKE

### Kubernetes & Helm
- [X] All deployments are Helm-based
- [X] Helm values allow environment separation (local vs cloud)
- [X] Helm values allow replica scaling and resource limits

### CI/CD Automation
- [X] GitHub Actions build Docker images
- [X] GitHub Actions push images to registry
- [X] GitHub Actions deploy via Helm
- [X] No manual production deployments

### Observability & Reliability
- [X] Logging and monitoring enabled
- [X] Failures are recoverable without data loss
- [X] System tolerates Pod restarts, horizontal scaling, event replays

## Gates Evaluation

### Gate 1: Spec-Driven Compliance ✅
- All changes documented in speckit.specify → speckit.plan → speckit.tasks
- No implementation without proper specification

### Gate 2: Cloud-Native Architecture ✅
- All services designed to be stateless
- Horizontal scaling capabilities planned
- Kubernetes-native deployment approach

### Gate 3: Event-Driven Architecture ✅
- Kafka access only through Dapr Pub/Sub
- Event flow designed for task lifecycle events
- No direct service-to-service coupling

### Gate 4: Dapr Integration ✅
- All infrastructure access through Dapr building blocks
- No hardcoded credentials or service URLs
- Proper abstraction layer implemented

### Gate 5: Container-First Design ✅
- All services packaged as containers
- Helm-based deployment strategy
- Environment-agnostic configuration

### Gate 6: Advanced Services Separation ✅
- Recurring Task Service as separate component
- Notification Service as separate component
- Audit Service as separate component
- Each service has single responsibility

## Project Structure

### Documentation (this feature)

```text
specs/001-cloud-native-todo/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application with multiple backend services
backend/
├── chat-api/            # Chat API Service (FastAPI + OpenAI Agents SDK + MCP)
│   ├── src/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── dapr_client/
│   ├── Dockerfile
│   └── requirements.txt
├── recurring-task-service/  # Recurring Task Service
│   ├── src/
│   │   ├── main.py
│   │   └── consumers/
│   ├── Dockerfile
│   └── requirements.txt
├── notification-service/    # Notification Service
│   ├── src/
│   │   ├── main.py
│   │   └── consumers/
│   ├── Dockerfile
│   └── requirements.txt
├── audit-service/           # Audit Service
│   ├── src/
│   │   ├── main.py
│   │   └── consumers/
│   ├── Dockerfile
│   └── requirements.txt
└── shared/                # Shared libraries and utilities
    ├── models/
    ├── utils/
    └── dapr_components/

frontend/
├── src/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── types/
├── Dockerfile
└── package.json

helm/
├── todo-chatbot/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── frontend/
│       ├── chat-api/
│       ├── recurring-task-service/
│       ├── notification-service/
│       ├── audit-service/
│       └── dapr-components/
└── infrastructure/
    ├── Chart.yaml
    ├── values.yaml
    └── templates/
        ├── kafka/
        ├── postgresql/
        └── redis/

dapr/
└── components/
    ├── pubsub.yaml        # Kafka pub/sub component
    ├── statestore.yaml    # PostgreSQL state store
    ├── secrets.yaml       # Secret store component
    └── jobs.yaml          # Jobs API component
```

**Structure Decision**: Selected web application with multiple backend services architecture to support the event-driven, decoupled system requirements. Each service has its own Dockerfile and follows the cloud-native architecture principles outlined in the specification.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple backend services | Event-driven architecture requires decoupled services | Single monolithic service would violate event-driven principle |

## Post-Design Constitution Check

After implementing the design elements, we re-evaluate compliance with the constitution:

### Spec-Driven Only ✅ COMPLIANT
- [X] All changes documented in speckit.specify → speckit.plan → speckit.tasks
- [X] No implementation without proper specification
- [X] All architectural decisions documented in specs

### Cloud-Native Architecture ✅ COMPLIANT
- [X] All services designed to be stateless
- [X] All services designed for horizontal scalability
- [X] All services are Kubernetes-native
- [X] Communication uses event-driven (Kafka via Dapr) and service invocation via Dapr

### Event-Driven First (Kafka + Dapr) ✅ COMPLIANT
- [X] All task lifecycle events emit domain events (created, updated, completed, deleted)
- [X] Kafka accessed ONLY through Dapr
- [X] Dapr Pub/Sub is the ONLY interface for events
- [X] Event schema defined and documented

### Advanced Features via Decoupled Services ✅ COMPLIANT
- [X] Recurring Task Engine implemented as separate service
- [X] Reminder/Notification Service implemented as separate service
- [X] Audit/Activity Log Service implemented as separate service
- [X] Each service performs single responsibility and can be independently scaled

### Dapr as the Infrastructure Abstraction Layer ✅ COMPLIANT
- [X] Application code does NOT import Kafka clients
- [X] Application code does NOT embed database credentials
- [X] Application code does NOT hardcode service URLs
- [X] Applications use Dapr Pub/Sub, State Store, Jobs API, Service Invocation, and Secrets
- [X] Dapr components properly configured

### Docker & Containers ✅ COMPLIANT
- [X] All services run as containers
- [X] Dockerfiles generated for each service
- [X] Local runtime: Minikube
- [X] Cloud runtime: AKS / GKE / OKE

### Kubernetes & Helm ✅ COMPLIANT
- [X] All deployments are Helm-based
- [X] Helm values allow environment separation (local vs cloud)
- [X] Helm values allow replica scaling and resource limits
- [X] Infrastructure and application charts properly structured

### CI/CD Automation ✅ COMPLIANT
- [X] GitHub Actions build Docker images
- [X] GitHub Actions push images to registry
- [X] GitHub Actions deploy via Helm
- [X] No manual production deployments

### Observability & Reliability ✅ COMPLIANT
- [X] Logging and monitoring enabled through Dapr
- [X] Failures are recoverable without data loss
- [X] System tolerates Pod restarts, horizontal scaling, event replays
- [X] Services are designed to be idempotent for event replay safety