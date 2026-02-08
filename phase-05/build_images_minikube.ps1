# PowerShell script to set Docker environment to Minikube and build images

# Set Docker environment to use Minikube's Docker daemon
$env:DOCKER_TLS_VERIFY = "1"
$env:DOCKER_HOST = "tcp://127.0.0.1:53655"  # This is from the minikube docker-env command
$env:DOCKER_CERT_PATH = "$env:USERPROFILE\.minikube\certs"
$env:MINIKUBE_ACTIVE_DOCKERD = "minikube"

Write-Host "Docker environment set to Minikube" -ForegroundColor Green

# Build the audit-service
Write-Host "Building audit-service..." -ForegroundColor Yellow
Set-Location backend/audit-service
docker build -t todo-chatbot/audit-service:latest -f Dockerfile .
if ($LASTEXITCODE -ne 0) { throw "Failed to build audit-service" }
Set-Location ../..

# Build the chat-api service
Write-Host "Building chat-api service..." -ForegroundColor Yellow
Set-Location backend/chat-api
docker build -t todo-chatbot/chat-api:latest -f Dockerfile .
if ($LASTEXITCODE -ne 0) { throw "Failed to build chat-api" }
Set-Location ../..

# Build the notification-service
Write-Host "Building notification-service..." -ForegroundColor Yellow
Set-Location backend/notification-service
docker build -t todo-chatbot/notification-service:latest -f Dockerfile .
if ($LASTEXITCODE -ne 0) { throw "Failed to build notification-service" }
Set-Location ../..

# Build the recurring-task-service
Write-Host "Building recurring-task-service..." -ForegroundColor Yellow
Set-Location backend/recurring-task-service
docker build -t todo-chatbot/recurring-task-service:latest -f Dockerfile .
if ($LASTEXITCODE -ne 0) { throw "Failed to build recurring-task-service" }
Set-Location ../..

# Build the frontend
Write-Host "Building frontend..." -ForegroundColor Yellow
Set-Location frontend
docker build -t todo-chatbot/frontend:latest -f Dockerfile .
if ($LASTEXITCODE -ne 0) { throw "Failed to build frontend" }
Set-Location ..

# Build the main todo-chatbot image
Write-Host "Building main todo-chatbot image..." -ForegroundColor Yellow
docker build -t todo-chatbot:latest . -f backend/chat-api/Dockerfile
if ($LASTEXITCODE -ne 0) { throw "Failed to build main todo-chatbot image" }

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