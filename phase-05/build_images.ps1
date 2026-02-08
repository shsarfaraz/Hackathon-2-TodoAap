# PowerShell script to build all Docker images for the Todo Chatbot services

Write-Host "Building Docker images for Todo Chatbot services..." -ForegroundColor Green

# Build the audit-service
Write-Host "Building audit-service..." -ForegroundColor Yellow
Set-Location backend/audit-service
docker build -t todo-chatbot/audit-service:latest -f Dockerfile .
Set-Location ../..

# Build the chat-api service
Write-Host "Building chat-api service..." -ForegroundColor Yellow
Set-Location backend/chat-api
docker build -t todo-chatbot/chat-api:latest -f Dockerfile .
Set-Location ../..

# Build the notification-service
Write-Host "Building notification-service..." -ForegroundColor Yellow
Set-Location backend/notification-service
docker build -t todo-chatbot/notification-service:latest -f Dockerfile .
Set-Location ../..

# Build the recurring-task-service
Write-Host "Building recurring-task-service..." -ForegroundColor Yellow
Set-Location backend/recurring-task-service
docker build -t todo-chatbot/recurring-task-service:latest -f Dockerfile .
Set-Location ../..

# Build the frontend
Write-Host "Building frontend..." -ForegroundColor Yellow
Set-Location frontend
docker build -t todo-chatbot/frontend:latest -f Dockerfile .
Set-Location ..

# Build the main todo-chatbot image
Write-Host "Building main todo-chatbot image..." -ForegroundColor Yellow
docker build -t todo-chatbot:latest . -f backend/chat-api/Dockerfile

Write-Host "All Docker images built successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Built images:" -ForegroundColor Cyan
Write-Host "- todo-chatbot/audit-service:latest"
Write-Host "- todo-chatbot/chat-api:latest"
Write-Host "- todo-chatbot/notification-service:latest"
Write-Host "- todo-chatbot/recurring-task-service:latest"
Write-Host "- todo-chatbot/frontend:latest"
Write-Host "- todo-chatbot:latest"
Write-Host ""
Write-Host "You can now deploy the application using the Kubernetes manifests." -ForegroundColor Green