# Deploying Todo Chatbot Application Without Helm

This document provides instructions for deploying the Todo Chatbot application when Helm is not available due to organizational policies or other restrictions.

## Overview

Due to Helm being blocked by organizational Device Guard policy, we provide an alternative approach to deploy the Todo Chatbot application using raw Kubernetes manifests generated from the Helm templates.

## Prerequisites

Before deploying the application, ensure you have:

1. A running Minikube cluster
2. Dapr installed and running in the cluster
3. `kubectl` installed and configured to connect to your Minikube cluster
4. Docker images for all services built and available (or use placeholder images that will be pulled)

## Deployment Steps

### 1. Prepare Infrastructure Components

The Todo Chatbot application requires external infrastructure components:

- PostgreSQL database
- Kafka for messaging (via Dapr pub/sub)

If you don't have these services running, you can deploy them using Helm charts:

```bash
# Add required Helm repositories
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

### 2. Generate and Apply Kubernetes Manifests

Run the deployment script to generate Kubernetes manifests and apply them:

```bash
# Make the script executable
chmod +x deploy_without_helm.sh

# Run the deployment script
./deploy_without_helm.sh
```

Alternatively, you can manually apply the manifests:

```bash
# Apply Dapr components first
kubectl apply -f generated-manifests/dapr-components.yaml

# Apply application services
kubectl apply -f generated-manifests/chat-api.yaml
kubectl apply -f generated-manifests/recurring-task-service.yaml
kubectl apply -f generated-manifests/notification-service.yaml
kubectl apply -f generated-manifests/audit-service.yaml
kubectl apply -f generated-manifests/frontend.yaml

# Apply main deployment and service
kubectl apply -f generated-manifests/deployment.yaml
kubectl apply -f generated-manifests/service.yaml
```

### 3. Verify the Deployment

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

### 4. Access the Application

Once all services are running, you can access the frontend:

```bash
kubectl port-forward svc/todo-chatbot-frontend 3000:80
```

Then navigate to `http://localhost:3000` in your browser.

## Troubleshooting

### Common Issues

1. **Pods stuck in Pending state**: Check if you have sufficient resources in your Minikube cluster
   ```bash
   minikube ssh
   df -h  # Check disk space
   free -h  # Check memory
   ```

2. **ImagePullBackOff errors**: Ensure your Docker images are available in a registry accessible to your cluster

3. **Dapr sidecars not injected**: Verify that Dapr is properly installed and running:
   ```bash
   kubectl get pods -n dapr-system
   ```

4. **Service connections failing**: Check that services are properly named and that Dapr service invocation is working

### Checking Logs

To debug issues, check the logs of your pods:

```bash
kubectl logs -l app.kubernetes.io/name=todo-chatbot
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
kubectl set image deployment/todo-chatbot-chat-api chat-api=new-image:tag
kubectl set image deployment/todo-chatbot-frontend frontend=new-image:tag
```

Then restart the deployments:

```bash
kubectl rollout restart deployment/todo-chatbot-chat-api
kubectl rollout restart deployment/todo-chatbot-frontend
```

## Cleanup

To remove the application:

```bash
kubectl delete -f generated-manifests/
```

Or remove individual components:

```bash
kubectl delete deployment todo-chatbot
kubectl delete service todo-chatbot
kubectl delete deployment todo-chatbot-chat-api
kubectl delete service todo-chatbot-chat-api
# ... and so on for other services
```

## Notes

- The generated manifests use placeholder values that may need to be adjusted for your specific environment
- Ensure that the database connection strings and other configuration parameters match your infrastructure setup
- The Dapr components are configured to work with Kafka and PostgreSQL as specified in the original design
- For production deployments, consider using more restrictive RBAC settings and security configurations