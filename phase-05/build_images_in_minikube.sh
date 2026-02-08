#!/bin/bash

# Script to build Docker images inside Minikube VM
# This avoids certificate issues by building directly in the Minikube environment

echo "Building Docker images inside Minikube VM..."

# Build the audit-service
echo "Building audit-service..."
minikube ssh "cd /host_mnt/e/GenerativeAI/hackathon--2/hackathon_2/phase-05/backend/audit-service && docker build -t todo-chatbot/audit-service:latest -f Dockerfile ."

# Build the chat-api service
echo "Building chat-api service..."
minikube ssh "cd /host_mnt/e/GenerativeAI/hackathon--2/hackathon_2/phase-05/backend/chat-api && docker build -t todo-chatbot/chat-api:latest -f Dockerfile ."

# Build the notification-service
echo "Building notification-service..."
minikube ssh "cd /host_mnt/e/GenerativeAI/hackathon--2/hackathon_2/phase-05/backend/notification-service && docker build -t todo-chatbot/notification-service:latest -f Dockerfile ."

# Build the recurring-task-service
echo "Building recurring-task-service..."
minikube ssh "cd /host_mnt/e/GenerativeAI/hackathon--2/hackathon_2/phase-05/backend/recurring-task-service && docker build -t todo-chatbot/recurring-task-service:latest -f Dockerfile ."

# Build the frontend
echo "Building frontend..."
minikube ssh "cd /host_mnt/e/GenerativeAI/hackathon--2/hackathon_2/phase-05/frontend && docker build -t todo-chatbot/frontend:latest -f Dockerfile ."

# Build the main todo-chatbot image
echo "Building main todo-chatbot image..."
minikube ssh "cd /host_mnt/e/GenerativeAI/hackathon--2/hackathon_2/phase-05 && docker build -t todo-chatbot:latest . -f backend/chat-api/Dockerfile"

echo "All Docker images built successfully inside Minikube!"
echo ""
echo "Built images:"
echo "- todo-chatbot/audit-service:latest"
echo "- todo-chatbot/chat-api:latest"
echo "- todo-chatbot/notification-service:latest"
echo "- todo-chatbot/recurring-task-service:latest"
echo "- todo-chatbot/frontend:latest"
echo "- todo-chatbot:latest"
echo ""
echo "Images are now available in the Minikube cluster."