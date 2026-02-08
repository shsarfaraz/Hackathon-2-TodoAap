#!/bin/bash

# Script to generate Kubernetes manifests from Helm templates and deploy directly with kubectl
# This is an alternative approach when Helm is blocked by organizational policy

set -e  # Exit on any error

echo "Generating Kubernetes manifests from Helm templates..."

# Create a temporary directory for the generated manifests
TEMP_DIR="./generated-manifests"
mkdir -p $TEMP_DIR

# Generate manifests by substituting Helm template values manually
# This is a simplified approach - in a real scenario, you'd want to properly template these

# Copy the templates with default values substituted
echo "Creating Deployment manifest..."
cat << EOF > $TEMP_DIR/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-chatbot
  labels:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: todo-chatbot
      app.kubernetes.io/instance: todo-chatbot
  template:
    metadata:
      labels:
        app.kubernetes.io/name: todo-chatbot
        app.kubernetes.io/instance: todo-chatbot
    spec:
      containers:
        - name: todo-chatbot
          image: your-chatbot-image:latest
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
          resources:
            limits:
              cpu: 500m
              memory: 512Mi
            requests:
              cpu: 250m
              memory: 256Mi
EOF

echo "Creating Service manifest..."
cat << EOF > $TEMP_DIR/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-chatbot
  labels:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8080
      protocol: TCP
      name: http
  selector:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
EOF

echo "Creating Chat API Deployment and Service..."
cat << EOF > $TEMP_DIR/chat-api.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-chatbot-chat-api
  labels:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app: chat-api
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: todo-chatbot
      app.kubernetes.io/instance: todo-chatbot
      app: chat-api
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "chat-api"
        dapr.io/app-port: "8000"
        dapr.io/config: "tracing"
        dapr.io/protocol: "grpc"
      labels:
        app.kubernetes.io/name: todo-chatbot
        app.kubernetes.io/instance: todo-chatbot
        app: chat-api
    spec:
      containers:
        - name: chat-api
          image: todo-chatbot/chat-api:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              value: "postgresql://postgres:supersecurepassword@postgresql-postgresql.primary.svc.cluster.local:5432/postgres?sslmode=disable"
            - name: PYTHONPATH
              value: "/app/src"
          resources:
            limits:
              cpu: 500m
              memory: 512Mi
            requests:
              cpu: 250m
              memory: 256Mi
---
apiVersion: v1
kind: Service
metadata:
  name: todo-chatbot-chat-api
  labels:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app: chat-api
spec:
  type: ClusterIP
  ports:
    - port: 8000
      targetPort: 8000
      protocol: TCP
      name: http
  selector:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app: chat-api
EOF

echo "Creating Recurring Task Service Deployment and Service..."
cat << EOF > $TEMP_DIR/recurring-task-service.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-chatbot-recurring-task-service
  labels:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app: recurring-task-service
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: todo-chatbot
      app.kubernetes.io/instance: todo-chatbot
      app: recurring-task-service
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "recurring-task-service"
        dapr.io/app-port: "50001"
        dapr.io/config: "tracing"
        dapr.io/protocol: "grpc"
      labels:
        app.kubernetes.io/name: todo-chatbot
        app.kubernetes.io/instance: todo-chatbot
        app: recurring-task-service
    spec:
      containers:
        - name: recurring-task-service
          image: todo-chatbot/recurring-task-service:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 50001
          env:
            - name: DATABASE_URL
              value: "postgresql://postgres:supersecurepassword@postgresql-postgresql.primary.svc.cluster.local:5432/postgres?sslmode=disable"
            - name: PYTHONPATH
              value: "/app/src"
          resources:
            limits:
              cpu: 300m
              memory: 256Mi
            requests:
              cpu: 150m
              memory: 128Mi
---
apiVersion: v1
kind: Service
metadata:
  name: todo-chatbot-recurring-task-service
  labels:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app: recurring-task-service
spec:
  type: ClusterIP
  ports:
    - port: 50001
      targetPort: 50001
      protocol: TCP
      name: grpc
  selector:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app: recurring-task-service
EOF

echo "Creating Notification Service Deployment and Service..."
cat << EOF > $TEMP_DIR/notification-service.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-chatbot-notification-service
  labels:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app: notification-service
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: todo-chatbot
      app.kubernetes.io/instance: todo-chatbot
      app: notification-service
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "notification-service"
        dapr.io/app-port: "50001"
        dapr.io/config: "tracing"
        dapr.io/protocol: "grpc"
      labels:
        app.kubernetes.io/name: todo-chatbot
        app.kubernetes.io/instance: todo-chatbot
        app: notification-service
    spec:
      containers:
        - name: notification-service
          image: todo-chatbot/notification-service:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 50001
          env:
            - name: DATABASE_URL
              value: "postgresql://postgres:supersecurepassword@postgresql-postgresql.primary.svc.cluster.local:5432/postgres?sslmode=disable"
            - name: PYTHONPATH
              value: "/app/src"
          resources:
            limits:
              cpu: 300m
              memory: 256Mi
            requests:
              cpu: 150m
              memory: 128Mi
---
apiVersion: v1
kind: Service
metadata:
  name: todo-chatbot-notification-service
  labels:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app: notification-service
spec:
  type: ClusterIP
  ports:
    - port: 50001
      targetPort: 50001
      protocol: TCP
      name: grpc
  selector:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app: notification-service
EOF

echo "Creating Audit Service Deployment and Service..."
cat << EOF > $TEMP_DIR/audit-service.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-chatbot-audit-service
  labels:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app: audit-service
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: todo-chatbot
      app.kubernetes.io/instance: todo-chatbot
      app: audit-service
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "audit-service"
        dapr.io/app-port: "50001"
        dapr.io/config: "tracing"
        dapr.io/protocol: "grpc"
      labels:
        app.kubernetes.io/name: todo-chatbot
        app.kubernetes.io/instance: todo-chatbot
        app: audit-service
    spec:
      containers:
        - name: audit-service
          image: todo-chatbot/audit-service:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 50001
          env:
            - name: DATABASE_URL
              value: "postgresql://postgres:supersecurepassword@postgresql-postgresql.primary.svc.cluster.local:5432/postgres?sslmode=disable"
            - name: PYTHONPATH
              value: "/app/src"
          resources:
            limits:
              cpu: 300m
              memory: 256Mi
            requests:
              cpu: 150m
              memory: 128Mi
---
apiVersion: v1
kind: Service
metadata:
  name: todo-chatbot-audit-service
  labels:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app: audit-service
spec:
  type: ClusterIP
  ports:
    - port: 50001
      targetPort: 50001
      protocol: TCP
      name: grpc
  selector:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app: audit-service
EOF

echo "Creating Frontend Deployment and Service..."
cat << EOF > $TEMP_DIR/frontend.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-chatbot-frontend
  labels:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: todo-chatbot
      app.kubernetes.io/instance: todo-chatbot
      app: frontend
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "frontend"
        dapr.io/app-port: "3000"
        dapr.io/config: "tracing"
        dapr.io/protocol: "grpc"
      labels:
        app.kubernetes.io/name: todo-chatbot
        app.kubernetes.io/instance: todo-chatbot
        app: frontend
    spec:
      containers:
        - name: frontend
          image: todo-chatbot/frontend:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 3000
          env:
            - name: NEXT_PUBLIC_API_BASE_URL
              value: "http://todo-chatbot-chat-api:8000"
          resources:
            limits:
              cpu: 300m
              memory: 256Mi
            requests:
              cpu: 150m
              memory: 128Mi
---
apiVersion: v1
kind: Service
metadata:
  name: todo-chatbot-frontend
  labels:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app: frontend
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 3000
      protocol: TCP
      name: http
  selector:
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app: frontend
EOF

echo "Creating Dapr Components..."
cat << EOF > $TEMP_DIR/dapr-components.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "my-cluster-kafka-brokers.kafka:9092"  # Kafka broker address
  - name: consumerGroup
    value: "dapr-consumer-group"  # Consumer group for Dapr
  - name: clientID
    value: "dapr-client"
  - name: authRequired
    value: "false"  # Set to "true" if authentication is required
---
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    value: "host=postgresql-postgresql.primary.svc.cluster.local user=postgres password=supersecurepassword port=5432 database=postgres sslmode=disable"
  - name: actorStateStore
    value: "true"
---
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: secrets
spec:
  type: secretstores.kubernetes
  version: v1
  metadata:
  - name: namespace
    value: "default"
---
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: jobs
spec:
  type: bindings.cron
  version: v1
  metadata:
  - name: schedule
    value: "*/30 * * * *"  # Example cron schedule - runs every 30 minutes
EOF

echo ""
echo "Generated Kubernetes manifests have been created in the $TEMP_DIR directory."
echo ""
echo "To deploy the application, run the following commands:"
echo ""
echo "# Apply Dapr components first"
echo "kubectl apply -f $TEMP_DIR/dapr-components.yaml"
echo ""
echo "# Apply all other resources"
echo "kubectl apply -f $TEMP_DIR/"
echo ""
echo "To verify the deployment:"
echo "kubectl get pods"
echo "kubectl get services"
echo "kubectl get pods -l app.kubernetes.io/name=todo-chatbot"
echo ""
echo "To check Dapr sidecars:"
echo "kubectl get pods -o yaml | grep dapr"
echo ""
echo "To access the frontend service (after deployment is complete):"
echo "kubectl port-forward svc/todo-chatbot-frontend 3000:80"
echo ""
echo "Note: You may need to deploy infrastructure components like PostgreSQL and Kafka before deploying the application."