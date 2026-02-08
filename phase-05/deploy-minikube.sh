#!/bin/bash

# Deployment script for Todo Chatbot on Kubernetes with Dapr

set -e  # Exit on any error

echo "Starting deployment of Todo Chatbot to Kubernetes with Dapr..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed. Please install kubectl and configure your Kubernetes cluster."
    exit 1
fi

# Check if dapr CLI is available
if ! command -v dapr &> /dev/null; then
    echo "dapr CLI is not installed. Please install Dapr CLI."
    exit 1
fi

# Check if helm is available
if ! command -v helm &> /dev/null; then
    echo "helm is not installed. Please install Helm."
    exit 1
fi

echo "All required tools are available."

# Step 1: Initialize Dapr in the Kubernetes cluster
echo "Initializing Dapr in Kubernetes cluster..."
dapr init -k
kubectl wait --for=condition=ready pods --all -n dapr-system --timeout=300s
echo "Dapr initialized successfully."

# Step 2: Deploy infrastructure components (PostgreSQL, Kafka)
echo "Deploying infrastructure components..."

# Deploy PostgreSQL using Bitnami chart
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install postgresql bitnami/postgresql \
  --namespace postgresql \
  --create-namespace \
  --set auth.postgresPassword=supersecurepassword \
  --set primary.persistence.enabled=false

# Deploy Kafka using Strimzi
helm repo add strimzi https://strimzi.io/charts/
helm repo update
helm install strimzi strimzi/strimzi-kafka-operator --namespace kafka --create-namespace
kubectl apply -f ../dapr/components/kafka-cluster.yaml

echo "Infrastructure components deployed."

# Step 3: Wait for infrastructure to be ready
echo "Waiting for infrastructure to be ready..."
kubectl wait --for=condition=ready pods --all -n postgresql --timeout=300s
kubectl wait --for=condition=ready pods --all -n kafka --timeout=600s
echo "Infrastructure is ready."

# Step 4: Build and push Docker images
echo "Building and pushing Docker images..."

# Build chat-api service
docker build -t todo-chatbot/chat-api:latest -f ../../backend/chat-api/Dockerfile .

# Build recurring-task-service
docker build -t todo-chatbot/recurring-task-service:latest -f ../../backend/recurring-task-service/Dockerfile .

# Build notification-service
docker build -t todo-chatbot/notification-service:latest -f ../../backend/notification-service/Dockerfile .

# Build audit-service
docker build -t todo-chatbot/audit-service:latest -f ../../backend/audit-service/Dockerfile .

# Build frontend
docker build -t todo-chatbot/frontend:latest -f ../../frontend/Dockerfile .

# If using Minikube, load images directly into the cluster
if command -v minikube &> /dev/null; then
    minikube image load todo-chatbot/chat-api:latest
    minikube image load todo-chatbot/recurring-task-service:latest
    minikube image load todo-chatbot/notification-service:latest
    minikube image load todo-chatbot/audit-service:latest
    minikube image load todo-chatbot/frontend:latest
fi

echo "Docker images built successfully."

# Step 5: Deploy Dapr components
echo "Deploying Dapr components..."
kubectl apply -f ../../dapr/components/
echo "Dapr components deployed."

# Step 6: Deploy the application using Helm
echo "Deploying application using Helm..."
helm install todo-chatbot . --namespace todo-chatbot --create-namespace

# Wait for all pods to be ready
kubectl wait --for=condition=ready pods --all -n todo-chatbot --timeout=600s

echo "Application deployed successfully!"

# Step 7: Verify deployment
echo "Verifying deployment..."

# Check if all pods are running
echo "Checking pod status:"
kubectl get pods -n todo-chatbot

# Check Dapr sidecar injection
echo "Checking Dapr sidecars:"
kubectl get pods -n todo-chatbot -o yaml | grep dapr.io || true

# Port forward to access the frontend
echo "To access the application, run:"
echo "kubectl port-forward svc/todo-chatbot-frontend 3000:80 -n todo-chatbot"

echo "Deployment verification completed."

echo ""
echo "🎉 Todo Chatbot has been successfully deployed to Kubernetes with Dapr!"
echo ""
echo "Next steps:"
echo "1. Access the application: kubectl port-forward svc/todo-chatbot-frontend 3000:80 -n todo-chatbot"
echo "2. Visit http://localhost:3000 to use the application"
echo "3. Check service logs: kubectl logs -l app=chat-api -n todo-chatbot"
echo "4. Check Dapr logs: kubectl logs -l app=chat-api -n todo-chatbot -c daprd"