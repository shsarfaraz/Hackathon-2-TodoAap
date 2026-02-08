# Deployment Instructions for Todo Chatbot on Minikube

## Prerequisites

Before deploying the Todo Chatbot application, ensure you have the following tools installed:

- Docker Desktop
- Minikube
- kubectl
- Helm
- Dapr CLI

## Step-by-Step Deployment

### 1. Start Minikube

```bash
minikube start
```

### 2. Enable Dapr in Minikube

```bash
dapr init -k
kubectl wait --for=condition=ready pods --all -n dapr-system --timeout=300s
```

### 3. Deploy Infrastructure Components

#### Deploy PostgreSQL
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install postgresql bitnami/postgresql \
  --namespace postgresql \
  --create-namespace \
  --set auth.postgresPassword=supersecurepassword \
  --set primary.persistence.enabled=false
```

#### Deploy Kafka (for pub/sub messaging)
```bash
helm repo add strimzi https://strimzi.io/charts/
helm repo update
helm install strimzi strimzi/strimzi-kafka-operator --namespace kafka --create-namespace
kubectl apply -f - << EOF
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
EOF
```

### 4. Wait for Infrastructure to be Ready

```bash
kubectl wait --for=condition=ready pods --all -n postgresql --timeout=300s
kubectl wait --for=condition=ready pods --all -n kafka --timeout=600s
```

### 5. Build Docker Images

Since we're using Minikube, we need to build the images in the Minikube Docker environment:

```bash
# Set Docker environment to use Minikube's Docker daemon
eval $(minikube -p minikube docker-env)

# Build the audit-service
cd backend/audit-service
docker build -t todo-chatbot/audit-service:latest -f Dockerfile .
cd ../..

# Build the chat-api service
cd backend/chat-api
docker build -t todo-chatbot/chat-api:latest -f Dockerfile .
cd ../..

# Build the notification-service
cd backend/notification-service
docker build -t todo-chatbot/notification-service:latest -f Dockerfile .
cd ../..

# Build the recurring-task-service
cd backend/recurring-task-service
docker build -t todo-chatbot/recurring-task-service:latest -f Dockerfile .
cd ../..

# Build the frontend
cd frontend
docker build -t todo-chatbot/frontend:latest -f Dockerfile .
cd ..
```

### 6. Apply Dapr Components

```bash
kubectl apply -f rendered_final_fixed.yaml -l kind=Component
```

### 7. Deploy the Application

```bash
kubectl apply -f rendered_final_fixed.yaml
```

### 8. Wait for All Pods to be Ready

```bash
kubectl wait --for=condition=ready pods --all -n default --timeout=600s
```

### 9. Verify the Deployment

```bash
# Check pod status
kubectl get pods

# Check service status
kubectl get services

# Check Dapr sidecar injection
kubectl get pods -o yaml | grep dapr.io || true
```

### 10. Access the Application

```bash
# Port forward to access the frontend
kubectl port-forward svc/todo-chatbot-frontend 3000:80
```

Then navigate to `http://localhost:3000` in your browser to access the Todo Chatbot application.

### Troubleshooting

If you encounter any issues:

1. Check pod status: `kubectl get pods`
2. Check pod logs: `kubectl logs <pod-name>`
3. Check Dapr logs: `kubectl logs <pod-name> -c daprd`
4. Verify Dapr is running: `kubectl get pods -n dapr-system`

## Clean Up

To remove the application:

```bash
kubectl delete -f rendered_final_fixed.yaml
helm uninstall postgresql -n postgresql
helm uninstall strimzi -n kafka
kubectl delete namespace postgresql kafka
```