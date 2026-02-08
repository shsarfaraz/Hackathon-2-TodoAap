# Todo Chatbot Application Deployment Guide

This guide provides instructions for building and deploying the Todo Chatbot application with all its microservices.

## Prerequisites

- Docker installed and running
- Kubernetes cluster (Minikube recommended for local development)
- kubectl configured to connect to your cluster
- Dapr installed and running in your cluster

## Building the Docker Images

To build all Docker images for the services, run:

```bash
chmod +x build_images.sh
./build_images.sh
```

This will build Docker images for all services:
- `todo-chatbot/chat-api:latest`
- `todo-chatbot/recurring-task-service:latest`
- `todo-chatbot/notification-service:latest`
- `todo-chatbot/audit-service:latest`
- `todo-chatbot/frontend:latest`
- `todo-chatbot:latest`

## Deploying the Application

### 1. Deploy Infrastructure Components

First, ensure you have PostgreSQL and Kafka running in your cluster. You can deploy them using Helm:

```bash
# Add required repositories
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add strimzi https://strimzi.io/charts/
helm repo update

# Deploy PostgreSQL
helm install postgresql bitnami/postgresql \
  --namespace default \
  --set auth.postgresPassword=supersecurepassword \
  --set primary.persistence.enabled=false

# Deploy Kafka via Strimzi
helm install strimzi strimzi/strimzi-kafka-operator --namespace default
kubectl apply -f https://strimzi.io/examples/latest/kafka/kafka-ephemeral-single.yaml -n default
```

### 2. Deploy Dapr Components

Apply the Dapr components:

```bash
kubectl apply -f rendered_final.yaml -l app.kubernetes.io/managed-by=Helm -l app=pubsub
kubectl apply -f rendered_final.yaml -l app.kubernetes.io/managed-by=Helm -l app=statestore
kubectl apply -f rendered_final.yaml -l app.kubernetes.io/managed-by=Helm -l app=secrets
kubectl apply -f rendered_final.yaml -l app.kubernetes.io/managed-by=Helm -l app=jobs
```

### 3. Deploy the Application

Apply the complete application manifest:

```bash
kubectl apply -f rendered_final.yaml
```

### 4. Verify the Deployment

Check that all pods are running:

```bash
kubectl get pods
```

Check that all services are available:

```bash
kubectl get services
```

Check that Dapr sidecars are injected:

```bash
kubectl get pods -o yaml | grep dapr
```

## Accessing the Application

Once all services are running, you can access the frontend by port-forwarding:

```bash
kubectl port-forward svc/todo-chatbot-frontend 3000:80
```

Then navigate to `http://localhost:3000` in your browser.

## Troubleshooting

### Common Issues

1. **Pods stuck in Pending state**: Check if you have sufficient resources in your cluster
   ```bash
   kubectl describe nodes
   ```

2. **ImagePullBackOff errors**: Ensure your Docker images are built and available

3. **Dapr sidecars not injected**: Verify that Dapr is properly installed and running:
   ```bash
   kubectl get pods -n dapr-system
   ```

4. **Service connections failing**: Check that services are properly named and that Dapr service invocation is working

### Checking Logs

To debug issues, check the logs of your pods:

```bash
kubectl logs -l app=chat-api
kubectl logs -l app=recurring-task-service
kubectl logs -l app=notification-service
kubectl logs -l app=audit-service
kubectl logs -l app=frontend
```

Also check the Dapr sidecar logs:

```bash
kubectl logs -l app=chat-api -c daprd
kubectl logs -l app=recurring-task-service -c daprd
kubectl logs -l app=notification-service -c daprd
kubectl logs -l app=audit-service -c daprd
kubectl logs -l app=frontend -c daprd
```

## Scaling the Application

To scale any of the services, use the kubectl scale command:

```bash
kubectl scale deployment/todo-chatbot-chat-api --replicas=3
kubectl scale deployment/todo-chatbot-frontend --replicas=2
```

## Updating the Application

To update the application with new Docker images:

```bash
kubectl set image deployment/todo-chatbot-chat-api chat-api=todo-chatbot/chat-api:new-tag
kubectl set image deployment/todo-chatbot-frontend frontend=todo-chatbot/frontend:new-tag
```

Then restart the deployments:

```bash
kubectl rollout restart deployment/todo-chatbot-chat-api
kubectl rollout restart deployment/todo-chatbot-frontend
```

## Cleanup

To remove the application:

```bash
kubectl delete -f rendered_final.yaml
```

## Notes

- The rendered_final.yaml file contains all necessary Kubernetes resources for the application
- All services are configured with Dapr sidecars for event-driven communication
- The application follows a microservices architecture with proper service isolation
- For production deployments, consider using more restrictive RBAC settings and security configurations