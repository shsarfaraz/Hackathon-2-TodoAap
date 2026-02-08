# Todo Chatbot Helm Chart

This Helm chart deploys the Todo Chatbot application on Kubernetes.

## Chart Structure

The chart includes the following components:
- Main deployment and service for the todo-chatbot application
- Individual deployments for each microservice (chat-api, recurring-task-service, notification-service, audit-service)
- Frontend deployment
- Dapr component configurations
- Supporting resources (ConfigMaps, ServiceAccounts, Ingress)

## Configuration

The following values can be configured in `values.yaml`:

### Main Application
- `replicaCount`: Number of pod replicas (default: 1)
- `image.repository`: Container image repository
- `image.tag`: Container image tag
- `image.pullPolicy`: Image pull policy
- `service.type`: Service type (ClusterIP, NodePort, LoadBalancer)
- `service.port`: Service port
- `service.containerPort`: Container port
- `resources`: Resource limits and requests

### Service-Specific Configurations
- `chatApi`: Configuration for the chat API service
- `recurringTaskService`: Configuration for the recurring task service
- `notificationService`: Configuration for the notification service
- `auditService`: Configuration for the audit service
- `frontend`: Configuration for the frontend service

### Infrastructure
- `database`: Database connection configuration
- `dapr`: Dapr configuration
- `ingress`: Ingress configuration
- `serviceAccount`: Service account configuration

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
helm install my-release .
```

## Uninstalling the Chart

To uninstall/delete the `my-release` deployment:

```bash
helm delete my-release
```

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| replicaCount | int | 1 | Number of pod replicas |
| image.repository | string | "your-chatbot-image" | Container image repository |
| image.tag | string | "latest" | Container image tag |
| image.pullPolicy | string | "IfNotPresent" | Image pull policy |
| service.type | string | "ClusterIP" | Service type |
| service.port | int | 80 | Service port |
| service.containerPort | int | 8080 | Container port |
| resources.limits.cpu | string | "500m" | CPU resource limit |
| resources.limits.memory | string | "512Mi" | Memory resource limit |
| resources.requests.cpu | string | "250m" | CPU resource request |
| resources.requests.memory | string | "256Mi" | Memory resource request |
| serviceAccount.create | bool | true | Specifies whether a service account should be created |
| ingress.enabled | bool | false | Enable ingress |
| chatApi.replicaCount | int | 1 | Chat API service replica count |
| recurringTaskService.replicaCount | int | 1 | Recurring task service replica count |
| notificationService.replicaCount | int | 1 | Notification service replica count |
| auditService.replicaCount | int | 1 | Audit service replica count |
| frontend.replicaCount | int | 1 | Frontend service replica count |