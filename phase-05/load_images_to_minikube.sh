#!/bin/bash

# Script to load built Docker images into Minikube

set -e  # Exit on any error

echo "Loading Docker images into Minikube..."

# Load the images into Minikube
echo "Loading todo-chatbot/chat-api:latest into Minikube..."
minikube image load todo-chatbot/chat-api:latest

echo "Loading todo-chatbot/recurring-task-service:latest into Minikube..."
minikube image load todo-chatbot/recurring-task-service:latest

echo "Loading todo-chatbot/notification-service:latest into Minikube..."
minikube image load todo-chatbot/notification-service:latest

echo "Loading todo-chatbot/audit-service:latest into Minikube..."
minikube image load todo-chatbot/audit-service:latest

echo "Loading todo-chatbot/frontend:latest into Minikube..."
minikube image load todo-chatbot/frontend:latest

echo "All images loaded successfully into Minikube!"
echo ""
echo "You can now deploy the application using: kubectl apply -f rendered_final.yaml"