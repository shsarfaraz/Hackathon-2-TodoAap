# PowerShell script to build Docker images using Minikube's Docker daemon

# Set environment variables to use Minikube's Docker daemon
$env:DOCKER_TLS_VERIFY = "1"
$env:DOCKER_HOST = "tcp://127.0.0.1:53655"
$env:DOCKER_CERT_PATH = "$env:USERPROFILE\.minikube\certs"
$env:MINIKUBE_ACTIVE_DOCKERD = "minikube"

Write-Host "Setting up Docker environment to use Minikube's Docker daemon..." -ForegroundColor Green

# Test Docker connectivity
Write-Host "Testing Docker connectivity..." -ForegroundColor Yellow
try {
    docker version
    Write-Host "Docker connection successful!" -ForegroundColor Green
} catch {
    Write-Host "Failed to connect to Docker daemon: $_" -ForegroundColor Red
    exit 1
}

# Build the audit-service
Write-Host "Building audit-service..." -ForegroundColor Yellow
try {
    Set-Location backend/audit-service
    docker build -t todo-chatbot/audit-service:latest -f Dockerfile .
    Set-Location ../..
    Write-Host "audit-service built successfully!" -ForegroundColor Green
} catch {
    Write-Host "Failed to build audit-service: $_" -ForegroundColor Red
    exit 1
}

# Build the chat-api service
Write-Host "Building chat-api service..." -ForegroundColor Yellow
try {
    Set-Location backend/chat-api
    docker build -t todo-chatbot/chat-api:latest -f Dockerfile .
    Set-Location ../..
    Write-Host "chat-api built successfully!" -ForegroundColor Green
} catch {
    Write-Host "Failed to build chat-api: $_" -ForegroundColor Red
    exit 1
}

# Build the notification-service
Write-Host "Building notification-service..." -ForegroundColor Yellow
try {
    Set-Location backend/notification-service
    docker build -t todo-chatbot/notification-service:latest -f Dockerfile .
    Set-Location ../..
    Write-Host "notification-service built successfully!" -ForegroundColor Green
} catch {
    Write-Host "Failed to build notification-service: $_" -ForegroundColor Red
    exit 1
}

# Build the recurring-task-service
Write-Host "Building recurring-task-service..." -ForegroundColor Yellow
try {
    Set-Location backend/recurring-task-service
    docker build -t todo-chatbot/recurring-task-service:latest -f Dockerfile .
    Set-Location ../..
    Write-Host "recurring-task-service built successfully!" -ForegroundColor Green
} catch {
    Write-Host "Failed to build recurring-task-service: $_" -ForegroundColor Red
    exit 1
}

# Build the frontend
Write-Host "Building frontend..." -ForegroundColor Yellow
try {
    Set-Location frontend
    docker build -t todo-chatbot/frontend:latest -f Dockerfile .
    Set-Location ..
    Write-Host "frontend built successfully!" -ForegroundColor Green
} catch {
    Write-Host "Failed to build frontend: $_" -ForegroundColor Red
    exit 1
}

# Build the main todo-chatbot image
Write-Host "Building main todo-chatbot image..." -ForegroundColor Yellow
try {
    docker build -t todo-chatbot:latest . -f backend/chat-api/Dockerfile
    Write-Host "Main todo-chatbot image built successfully!" -ForegroundColor Green
} catch {
    Write-Host "Failed to build main todo-chatbot image: $_" -ForegroundColor Red
    exit 1
}

Write-Host "All Docker images built successfully in Minikube!" -ForegroundColor Green
Write-Host ""
Write-Host "Built images:" -ForegroundColor Cyan
Write-Host "- todo-chatbot/audit-service:latest"
Write-Host "- todo-chatbot/chat-api:latest"
Write-Host "- todo-chatbot/notification-service:latest"
Write-Host "- todo-chatbot/recurring-task-service:latest"
Write-Host "- todo-chatbot/frontend:latest"
Write-Host "- todo-chatbot:latest"
Write-Host ""
Write-Host "Images are now available in the Minikube cluster." -ForegroundColor Green