# Quickstart Guide: Evolution of Todo – Phase V (Advanced Cloud-Native Architecture)

## Overview
This guide provides instructions for setting up and running the cloud-native todo system locally using Minikube, Dapr, and Kafka. The system consists of multiple services that communicate via Dapr building blocks.

## Prerequisites

### System Requirements
- Windows 10/11, macOS, or Linux
- Docker Desktop (with Kubernetes enabled) or Minikube
- kubectl
- Helm 3+
- Dapr CLI
- .NET 6+ (for Dapr placement service)
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend services)

### Install Prerequisites

#### 1. Install Docker Desktop
Download and install Docker Desktop from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

#### 2. Install kubectl
Follow the instructions at [https://kubernetes.io/docs/tasks/tools/install-kubectl/](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

#### 3. Install Helm
Follow the instructions at [https://helm.sh/docs/intro/install/](https://helm.sh/docs/intro/install/)

#### 4. Install Dapr CLI
```bash
# Windows (using PowerShell)
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 -O install.ps1
.\install.ps1

# macOS/Linux
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | sh
```

#### 5. Install Minikube (if not using Docker Desktop Kubernetes)
```bash
# Windows
choco install minikube

# macOS
brew install minikube

# Linux
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
chmod +x minikube
sudo mv minikube /usr/local/bin
```

## Setting Up the Environment

### 1. Start Minikube (skip if using Docker Desktop Kubernetes)
```bash
minikube start --memory=8192 --cpus=4
```

### 2. Install Dapr on your Kubernetes cluster
```bash
dapr init -k
# Wait for Dapr to be ready
kubectl wait --for=condition=ready pods --all -n dapr-system --timeout=300s
```

### 3. Clone the repository
```bash
git clone https://github.com/your-org/todo-chatbot.git
cd todo-chatbot
```

### 4. Set up Kafka using Strimzi
```bash
# Add the Strimzi Helm repository
helm repo add strimzi https://strimzi.io/charts/
helm repo update

# Install Strimzi operator
helm install strimzi strimzi/strimzi-kafka-operator --namespace kafka --create-namespace

# Apply Kafka cluster configuration
kubectl apply -f ./dapr/components/kafka-cluster.yaml
```

### 5. Set up PostgreSQL using Bitnami chart
```bash
# Add the Bitnami Helm repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Install PostgreSQL
helm install postgresql bitnami/postgresql \
  --namespace postgresql \
  --create-namespace \
  --set auth.postgresPassword=supersecurepassword \
  --set primary.persistence.enabled=false
```

## Building and Deploying Services

### 1. Build Docker images for all services
```bash
# Build chat-api service
docker build -t todo-chatbot/chat-api:latest -f backend/chat-api/Dockerfile .

# Build recurring-task-service
docker build -t todo-chatbot/recurring-task-service:latest -f backend/recurring-task-service/Dockerfile .

# Build notification-service
docker build -t todo-chatbot/notification-service:latest -f backend/notification-service/Dockerfile .

# Build audit-service
docker build -t todo-chatbot/audit-service:latest -f backend/audit-service/Dockerfile .

# Build frontend
docker build -t todo-chatbot/frontend:latest -f frontend/Dockerfile .
```

### 2. Tag and push images to registry (for Minikube)
```bash
# If using Minikube, load images directly into the cluster
minikube image load todo-chatbot/chat-api:latest
minikube image load todo-chatbot/recurring-task-service:latest
minikube image load todo-chatbot/notification-service:latest
minikube image load todo-chatbot/audit-service:latest
minikube image load todo-chatbot/frontend:latest
```

### 3. Deploy infrastructure components
```bash
# Deploy Dapr components
kubectl apply -f ./dapr/components/ -n default
```

### 4. Deploy the application using Helm
```bash
# Install the main application chart
helm install todo-chatbot ./helm/todo-chatbot --namespace todo-chatbot --create-namespace
```

## Verifying the Deployment

### 1. Check if all pods are running
```bash
kubectl get pods -n todo-chatbot
```

Expected output should show all services running:
- frontend
- chat-api
- recurring-task-service
- notification-service
- audit-service

### 2. Check Dapr sidecar injection
```bash
kubectl get pods -n todo-chatbot -o yaml | grep dapr.io
```

### 3. Port forward to access the frontend
```bash
kubectl port-forward svc/frontend 3000:80 -n todo-chatbot
```

Visit [http://localhost:3000](http://localhost:3000) to access the application.

### 4. Check Dapr logs
```bash
kubectl logs -l app=chat-api -n todo-chatbot -c daprd
kubectl logs -l app=recurring-task-service -n todo-chatbot -c daprd
kubectl logs -l app=notification-service -n todo-chatbot -c daprd
kubectl logs -l app=audit-service -n todo-chatbot -c daprd
```

## Working with the Application

### 1. Register a new user
- Navigate to the application at [http://localhost:3000](http://localhost:3000)
- Click "Sign Up" and register a new account

### 2. Create a conversation
- After logging in, click "New Conversation" to start chatting with the AI assistant
- Ask the assistant to create tasks, update tasks, or manage your todo list

### 3. Create tasks
- Ask the AI assistant to create tasks like "Create a task to buy groceries"
- The assistant will create the task in the system

### 4. Set up recurring tasks
- Ask the AI assistant to create recurring tasks like "Create a daily task to drink water"
- The recurring task service will automatically generate new instances

### 5. Set reminders
- Ask the AI assistant to set reminders like "Remind me to call John tomorrow at 3 PM"
- The notification service will send a reminder at the specified time

## Troubleshooting

### Common Issues and Solutions

#### Issue: Dapr sidecar not injected
**Solution:** Check if the `dapr.io/enabled: "true"` annotation is present in the deployment YAML.

#### Issue: Kafka connection problems
**Solution:** Verify that the Kafka cluster is running and accessible:
```bash
kubectl get kafka -n kafka
kubectl logs -l strimzi.io/name=my-cluster-kafka -n kafka
```

#### Issue: PostgreSQL connection problems
**Solution:** Verify that PostgreSQL is running and accessible:
```bash
kubectl get pods -n postgresql
kubectl logs -l app.kubernetes.io/name=postgresql -n postgresql
```

#### Issue: Services not communicating
**Solution:** Check Dapr logs for errors and verify service invocation:
```bash
kubectl logs -l app=chat-api -n todo-chatbot -c daprd
```

### Useful Commands

#### Check all Dapr applications
```bash
dapr list -k
```

#### Get Dapr dashboard URL
```bash
dapr dashboard -k
```

#### Check Dapr components
```bash
kubectl get components -A
```

#### Check Dapr subscriptions
```bash
kubectl get subscriptions -A
```

## Scaling the Application

### Horizontal Pod Autoscaling
The application is configured with HPA. To check the status:
```bash
kubectl get hpa -n todo-chatbot
```

### Manually scale a service
```bash
kubectl scale deployment chat-api --replicas=3 -n todo-chatbot
```

## Cleaning Up

### Uninstall the application
```bash
helm uninstall todo-chatbot -n todo-chatbot
```

### Uninstall infrastructure
```bash
kubectl delete -f ./dapr/components/ -n default
helm uninstall postgresql -n postgresql
helm uninstall strimzi -n kafka
```

### Stop Minikube (if used)
```bash
minikube stop
```

## Next Steps

1. Explore the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs) for the chat API
2. Review the event-driven architecture and how services communicate via Dapr pub/sub
3. Customize the Dapr components in `./dapr/components/` to suit your needs
4. Extend the system by adding new services that subscribe to the existing topics
5. Deploy to a cloud Kubernetes cluster (AKS, GKE, or EKS) by updating the Helm values