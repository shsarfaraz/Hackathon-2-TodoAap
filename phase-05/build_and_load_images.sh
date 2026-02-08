#!/bin/bash

# Script to build and load Docker images for Todo Chatbot services into Minikube

set -e  # Exit on any error

echo "Setting Docker environment to Minikube..."
eval $(minikube -p minikube docker-env)

echo "Building Docker images for Todo Chatbot services..."

# Build the chat-api service
echo "Building chat-api service..."
cd backend/chat-api
docker build -t todo-chatbot/chat-api:latest .
cd ../..

# Build the recurring-task-service
echo "Building recurring-task-service..."
cd backend/recurring-task-service
docker build -t todo-chatbot/recurring-task-service:latest .
cd ../..

# Build the notification-service
echo "Building notification-service..."
cd backend/notification-service
docker build -t todo-chatbot/notification-service:latest .
cd ../..

# Build the audit-service
echo "Building audit-service..."
cd backend/audit-service
docker build -t todo-chatbot/audit-service:latest .
cd ../..

# Build the frontend
echo "Building frontend..."
cd frontend
docker build -t todo-chatbot/frontend:latest .
cd ..

echo "All Docker images built successfully in Minikube environment!"
echo ""
echo "Images built:"
echo "- todo-chatbot/chat-api:latest"
echo "- todo-chatbot/recurring-task-service:latest"
echo "- todo-chatbot/notification-service:latest"
echo "- todo-chatbot/audit-service:latest"
echo "- todo-chatbot/frontend:latest"
echo ""
echo "The images are already loaded in Minikube since we used Minikube's Docker environment."
echo ""
echo "You can now verify the images exist with: docker images | grep todo-chatbot"
echo "Then deploy the application using: kubectl apply -f rendered_final.yaml"