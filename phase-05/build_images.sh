#!/bin/bash

# Script to build all Docker images for the Todo Chatbot services

set -e  # Exit on any error

echo "Building Docker images for Todo Chatbot services..."

# Build the audit-service
echo "Building audit-service..."
cd backend/audit-service
docker build -t todo-chatbot/audit-service:latest -f Dockerfile .
cd ../..

# Build the chat-api service
echo "Building chat-api service..."
cd backend/chat-api
docker build -t todo-chatbot/chat-api:latest -f Dockerfile .
cd ../..

# Build the notification-service
echo "Building notification-service..."
cd backend/notification-service
docker build -t todo-chatbot/notification-service:latest -f Dockerfile .
cd ../..

# Build the recurring-task-service
echo "Building recurring-task-service..."
cd backend/recurring-task-service
docker build -t todo-chatbot/recurring-task-service:latest -f Dockerfile .
cd ../..

# Build the frontend
echo "Building frontend..."
cd frontend
docker build -t todo-chatbot/frontend:latest -f Dockerfile .
cd ..

# Build the main todo-chatbot image
echo "Building main todo-chatbot image..."
docker build -t todo-chatbot:latest . -f backend/chat-api/Dockerfile

echo "All Docker images built successfully!"
echo ""
echo "Built images:"
echo "- todo-chatbot/audit-service:latest"
echo "- todo-chatbot/chat-api:latest"
echo "- todo-chatbot/notification-service:latest"
echo "- todo-chatbot/recurring-task-service:latest"
echo "- todo-chatbot/frontend:latest"
echo "- todo-chatbot:latest"
echo ""
echo "You can now deploy the application using the Kubernetes manifests."