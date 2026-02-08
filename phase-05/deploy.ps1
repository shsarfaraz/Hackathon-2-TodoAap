# PowerShell Deployment Script for Todo Chatbot on Minikube

# Function to check if a command exists
function Test-CommandExists {
    param($command)
    $exists = $null -ne (Get-Command $command -ErrorAction SilentlyContinue)
    return $exists
}

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Green

$prerequisites = @("docker", "minikube", "kubectl", "helm", "dapr")
foreach ($tool in $prerequisites) {
    if (-not (Test-CommandExists $tool)) {
        Write-Host "$tool is not installed. Please install $tool before continuing." -ForegroundColor Red
        exit 1
    }
}

Write-Host "All prerequisites are installed." -ForegroundColor Green

# Step 1: Ensure Minikube is running
Write-Host "Ensuring Minikube is running..." -ForegroundColor Yellow
minikube status --format='{{.Host}}' 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Starting Minikube..." -ForegroundColor Yellow
    minikube start
} else {
    Write-Host "Minikube is already running." -ForegroundColor Green
}

# Step 2: Enable Dapr in Minikube
Write-Host "Installing Dapr in Kubernetes..." -ForegroundColor Yellow
dapr init -k
kubectl wait --for=condition=ready pods --all -n dapr-system --timeout=300s

# Step 3: Deploy Infrastructure Components

# Deploy PostgreSQL
Write-Host "Deploying PostgreSQL..." -ForegroundColor Yellow
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm upgrade --install postgresql bitnami/postgresql `
  --namespace postgresql `
  --create-namespace `
  --set auth.postgresPassword=supersecurepassword `
  --set primary.persistence.enabled=false

# Deploy Kafka
Write-Host "Deploying Kafka..." -ForegroundColor Yellow
helm repo add strimzi https://strimzi.io/charts/
helm repo update
helm upgrade --install strimzi strimzi/strimzi-kafka-operator --namespace kafka --create-namespace

# Create Kafka cluster
$kafkaYaml = @"
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
  namespace: kafka
spec:
  kafka:
    version: 3.8.0
    replicas: 1
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
      transaction.state.log.min.isr: 1
      default.replication.factor: 1
      min.insync.replicas: 1
      inter.broker.protocol.version: "3.8"
    storage:
      type: jbod
      volumes:
        - id: 0
          type: persistent-claim
          size: 10Gi
          deleteClaim: false
  zookeeper:
    replicas: 1
    storage:
      type: persistent-claim
      size: 5Gi
      deleteClaim: false
  entityOperator:
    topicOperator: {}
    userOperator: {}
"@

$kafkaYaml | Out-File -FilePath kafka-cluster.yaml -Encoding utf8
kubectl apply -f kafka-cluster.yaml
Remove-Item kafka-cluster.yaml

# Step 4: Wait for Infrastructure to be Ready
Write-Host "Waiting for infrastructure to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pods --all -n postgresql --timeout=300s
kubectl wait --for=condition=ready pods --all -n kafka --timeout=600s

# Step 5: Configure Docker to use Minikube's Docker daemon
Write-Host "Configuring Docker to use Minikube's Docker daemon..." -ForegroundColor Yellow
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# Step 6: Build Docker Images
Write-Host "Building Docker images..." -ForegroundColor Yellow

# Build the audit-service
Write-Host "Building audit-service..." -ForegroundColor Yellow
Push-Location backend/audit-service
docker build -t todo-chatbot/audit-service:latest -f Dockerfile .
Pop-Location

# Build the chat-api service
Write-Host "Building chat-api service..." -ForegroundColor Yellow
Push-Location backend/chat-api
docker build -t todo-chatbot/chat-api:latest -f Dockerfile .
Pop-Location

# Build the notification-service
Write-Host "Building notification-service..." -ForegroundColor Yellow
Push-Location backend/notification-service
docker build -t todo-chatbot/notification-service:latest -f Dockerfile .
Pop-Location

# Build the recurring-task-service
Write-Host "Building recurring-task-service..." -ForegroundColor Yellow
Push-Location backend/recurring-task-service
docker build -t todo-chatbot/recurring-task-service:latest -f Dockerfile .
Pop-Location

# Build the frontend
Write-Host "Building frontend..." -ForegroundColor Yellow
Push-Location frontend
docker build -t todo-chatbot/frontend:latest -f Dockerfile .
Pop-Location

# Step 7: Apply Dapr Components
Write-Host "Applying Dapr components..." -ForegroundColor Yellow
kubectl apply -f rendered_final_fixed.yaml -l kind=Component

# Step 8: Deploy the Application
Write-Host "Deploying the application..." -ForegroundColor Yellow
kubectl apply -f rendered_final_fixed.yaml

# Step 9: Wait for All Pods to be Ready
Write-Host "Waiting for all pods to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pods --all --all-namespaces --timeout=600s

# Step 10: Verify the Deployment
Write-Host "Verifying the deployment..." -ForegroundColor Green
kubectl get pods
kubectl get services
kubectl get pods -o yaml | Select-String "dapr.io" || Write-Host "No Dapr annotations found (this might be OK depending on your setup)"

Write-Host ""
Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To access the application, run:" -ForegroundColor Cyan
Write-Host "kubectl port-forward svc/todo-chatbot-frontend 3000:80" -ForegroundColor White
Write-Host ""
Write-Host "Then navigate to http://localhost:3000 in your browser." -ForegroundColor White