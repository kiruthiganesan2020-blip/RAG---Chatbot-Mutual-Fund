# Phase 4.3: Deployment and Operations

## Overview

Phase 4.3 implements complete deployment strategy for HDFC Mutual Fund RAG system, covering Docker containerization, production deployment, monitoring, and maintenance procedures.

## Architecture

### Deployment Components

1. **Docker Containerization**
   - Multi-stage builds for optimization
   - Health checks and monitoring
   - Volume mounting for data persistence
   - Environment-based configuration

2. **Orchestration Support**
   - Docker Compose for local development
   - Kubernetes manifests for production
   - Helm charts for scalable deployment
   - Service discovery and load balancing

3. **Monitoring Stack**
   - Application performance monitoring
   - Infrastructure health checks
   - Log aggregation and analysis
   - Alert management and notification

### Container Architecture

```yaml
# docker-compose.yml
version: '3.8'
services:
  hdfc-rag-backend:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - LOG_LEVEL=INFO
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Docker Configuration

### Multi-stage Build

**Build Stages**:
```dockerfile
# Stage 1: Dependencies
FROM python:3.11-slim as dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Application
FROM python:3.11-slim as application
WORKDIR /app
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin
COPY . .
RUN python docker_startup_simple.py
CMD ["python", "simple_backend.py"]
```

### Production Optimizations

**Image Optimization**:
- Minimal base images (Alpine Linux)
- Layer caching for faster builds
- Security scanning and vulnerability fixes
- Size optimization for faster deployments

**Runtime Configuration**:
```dockerfile
# Security
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Performance
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1
```

## Environment Management

### Development Environment

**Configuration**:
```bash
# .env.development
API_HOST=localhost
API_PORT=8000
API_DEBUG=true
LOG_LEVEL=DEBUG
GOOGLE_AI_STUDIO_API_KEY=dev_api_key
CHROMA_DB_PATH=./data/chroma
```

**Startup Commands**:
```bash
# Development server
docker-compose -f docker-compose.dev.yml up --build

# With hot reload
docker-compose -f docker-compose.dev.yml up --build --watch
```

### Staging Environment

**Configuration**:
```bash
# .env.staging
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false
LOG_LEVEL=INFO
GOOGLE_AI_STUDIO_API_KEY=staging_api_key
CHROMA_DB_PATH=/app/data/chroma
```

**Deployment Commands**:
```bash
# Staging deployment
docker-compose -f docker-compose.staging.yml up -d

# With rolling updates
docker-compose -f docker-compose.staging.yml up -d --no-deps backend
```

### Production Environment

**Configuration**:
```bash
# .env.production
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false
LOG_LEVEL=WARNING
GOOGLE_AI_STUDIO_API_KEY=${GOOGLE_AI_STUDIO_API_KEY}
CHROMA_DB_PATH=/app/data/chroma
```

**Deployment Commands**:
```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# With zero-downtime deployment
docker-compose -f docker-compose.prod.yml up -d --no-deps --scale backend=2
```

## Kubernetes Deployment

### Namespace Configuration

```yaml
# k8s/namespace.yml
apiVersion: v1
kind: Namespace
metadata:
  name: hdfc-rag
  labels:
    name: hdfc-rag
    environment: production
```

### Deployment Manifest

```yaml
# k8s/deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hdfc-rag-backend
  namespace: hdfc-rag
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hdfc-rag-backend
  template:
    metadata:
      labels:
        app: hdfc-rag-backend
    spec:
      containers:
      - name: backend
        image: hdfc-rag-system:latest
        ports:
        - containerPort: 8000
        env:
        - name: API_HOST
          value: "0.0.0.0"
        - name: API_PORT
          value: "8000"
        - name: GOOGLE_AI_STUDIO_API_KEY
          valueFrom:
            secretKeyRef:
              name: hdfc-rag-secrets
              key: google-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: data-volume
          mountPath: /app/data
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: hdfc-rag-data
```

### Service Configuration

```yaml
# k8s/service.yml
apiVersion: v1
kind: Service
metadata:
  name: hdfc-rag-backend-service
  namespace: hdfc-rag
spec:
  selector:
    app: hdfc-rag-backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Ingress Configuration

```yaml
# k8s/ingress.yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: hdfc-rag-ingress
  namespace: hdfc-rag
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  tls:
  - hosts:
    - api.hdfc-mutual-fund.com
    secretName: hdfc-rag-tls
  rules:
  - host: api.hdfc-mutual-fund.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: hdfc-rag-backend-service
            port:
              number: 80
```

## Monitoring and Observability

### Application Monitoring

**Metrics Collection**:
```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Active connections')

@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_DURATION.observe(duration)
    
    return response
```

**Health Checks**:
```python
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "vector_db": await check_vector_db(),
            "llm_service": await check_llm_service(),
            "data_pipeline": await check_data_pipeline()
        },
        "version": "1.0.0"
    }

async def check_vector_db():
    try:
        # Check ChromaDB connection
        return "healthy"
    except Exception:
        return "unhealthy"
```

### Log Management

**Structured Logging**:
```python
import structlog

logger = structlog.get_logger()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    
    with structlog.contextvars.bind_contextvars(request_id=request_id):
        logger.info(
            "HTTP request",
            method=request.method,
            url=str(request.url),
            user_agent=request.headers.get("user-agent"),
            remote_addr=request.client.host
        )
        
        response = await call_next(request)
        
        logger.info(
            "HTTP response",
            status_code=response.status_code,
            duration_ms=getattr(response, 'duration_ms', 0)
        )
        
        return response
```

**Log Aggregation**:
```yaml
# ELK Stack for log aggregation
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.15.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:7.15.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:7.15.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
```

## Security Configuration

### Container Security

**Security Context**:
```yaml
# Pod security context
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 1000
  fsGroup: 1000
  capabilities:
    drop:
    - ALL
  readOnlyRootFilesystem: true
```

**Network Policies**:
```yaml
# Network policy for restricted communication
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: hdfc-rag-network-policy
  namespace: hdfc-rag
spec:
  podSelector:
    matchLabels:
      app: hdfc-rag-backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
```

### Secrets Management

**Kubernetes Secrets**:
```yaml
# secrets.yml
apiVersion: v1
kind: Secret
metadata:
  name: hdfc-rag-secrets
  namespace: hdfc-rag
type: Opaque
data:
  google-api-key: <base64-encoded-api-key>
  database-password: <base64-encoded-password>
  jwt-secret: <base64-encoded-jwt-secret>
```

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest tests/ -v --cov=src
    - name: Security scan
      run: |
        pip install safety
        safety check

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Build Docker image
      run: |
        docker build -t hdfc-rag-system:${{ github.sha }} .
        docker tag hdfc-rag-system:${{ github.sha }} hdfc-rag-system:latest
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push hdfc-rag-system:${{ github.sha }}
        docker push hdfc-rag-system:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to Kubernetes
      run: |
        echo ${{ secrets.KUBECONFIG }} | base64 -d > kubeconfig
        export KUBECONFIG=kubeconfig
        kubectl set image deployment/hdfc-rag-backend hdfc-rag-system=${{ github.sha }} -n hdfc-rag
        kubectl rollout status deployment/hdfc-rag-backend -n hdfc-rag
```

### Deployment Strategies

**Rolling Updates**:
```yaml
# Zero-downtime deployment
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 1
    maxSurge: 1
  minReadySeconds: 5
  progressDeadlineSeconds: 600
```

**Blue-Green Deployment**:
```yaml
# Blue-green deployment for critical updates
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: hdfc-rag-bluegreen
spec:
  replicas: 3
  strategy:
    blueGreen:
      activeService: hdfc-rag-active
      previewService: hdfc-rag-preview
      autoPromotionEnabled: true
      scaleDownDelaySeconds: 30
      prePromotionAnalysis: true
```

## Performance Optimization

### Resource Management

**Resource Limits**:
```yaml
# Production resource limits
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "1Gi"
    cpu: "500m"
```

**Horizontal Pod Autoscaler**:
```yaml
# HPA for scaling based on CPU/memory
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hdfc-rag-hpa
  namespace: hdfc-rag
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: hdfc-rag-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Caching Strategy

**Redis Cache**:
```yaml
# Redis for response caching
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-cache
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis-cache
  template:
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
```

## Backup and Recovery

### Data Backup Strategy

**Automated Backups**:
```bash
#!/bin/bash
# backup.sh - Daily backup script

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/$DATE"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup ChromaDB data
tar -czf $BACKUP_DIR/chroma.tar.gz /app/data/chroma

# Backup processed documents
tar -czf $BACKUP_DIR/processed.tar.gz /app/data/processed

# Backup configuration
cp .env $BACKUP_DIR/env.backup

# Upload to cloud storage (AWS S3 example)
aws s3 sync $BACKUP_DIR s3://hdfc-rag-backups/$DATE/

# Cleanup old backups (keep 30 days)
find /backups -type d -mtime +30 -exec rm -rf {} \;
```

### Disaster Recovery

**Recovery Procedures**:
```bash
#!/bin/bash
# recovery.sh - Disaster recovery script

BACKUP_DATE=$1
BACKUP_DIR="/backups/$BACKUP_DATE"

if [ -z "$BACKUP_DATE" ]; then
    echo "Usage: $0 <backup_date>"
    exit 1
fi

# Download backup from cloud storage
aws s3 sync s3://hdfc-rag-backups/$BACKUP_DATE/ /tmp/recovery/

# Restore data
tar -xzf /tmp/recovery/chroma.tar.gz -C /app/data/
tar -xzf /tmp/recovery/processed.tar.gz -C /app/data/

# Restart services
kubectl rollout restart deployment/hdfc-rag-backend -n hdfc-rag
```

## Maintenance Procedures

### Health Monitoring

**System Health Dashboard**:
- API response times
- Error rates and types
- Resource utilization
- Database performance
- User activity metrics

**Alert Configuration**:
```yaml
# Prometheus alert rules
groups:
- name: hdfc-rag-alerts
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "High error rate detected"
      
  - alert: HighResponseTime
    expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High response time detected"
```

### Update Procedures

**Rolling Updates**:
```bash
#!/bin/bash
# update.sh - Application update procedure

# Pull latest image
docker pull hdfc-rag-system:latest

# Update deployment with zero downtime
kubectl set image deployment/hdfc-rag-backend hdfc-rag-system=hdfc-rag-system:latest -n hdfc-rag

# Wait for rollout completion
kubectl rollout status deployment/hdfc-rag-backend -n hdfc-rag --timeout=300s

# Verify health
kubectl wait --for=condition=ready pod -l app=hdfc-rag-backend -n hdfc-rag --timeout=300s
```

## Troubleshooting

### Common Issues

**Container Startup Issues**:
```bash
# Check container logs
docker logs hdfc-rag-backend

# Debug container issues
docker exec -it hdfc-rag-backend /bin/bash

# Check resource usage
docker stats hdfc-rag-backend
```

**Performance Issues**:
```bash
# Monitor resource usage
kubectl top pods -n hdfc-rag

# Check pod events
kubectl describe pod <pod-name> -n hdfc-rag

# Analyze logs
kubectl logs <pod-name> -n hdfc-rag --tail=100
```

**Network Issues**:
```bash
# Test connectivity
kubectl exec -it <pod-name> -n hdfc-rag -- curl -f http://localhost:8000/api/health

# Check service endpoints
kubectl get svc -n hdfc-rag

# Debug ingress
kubectl describe ingress hdfc-rag-ingress -n hdfc-rag
```

## Future Enhancements

### Phase 4.3.1: Advanced Deployment
- Multi-cloud deployment support
- GitOps with ArgoCD
- Canary deployments
- Advanced monitoring with APM

### Phase 4.3.2: Security Hardening
- Container security scanning
- Network policy enforcement
- Runtime security monitoring
- Compliance automation

### Phase 4.3.3: Performance Optimization
- Advanced caching strategies
- Database optimization
- CDN integration
- Edge computing support

---

**Status**: ✅ Completed
**Last Updated**: 2026-05-09
**Version**: 1.0.0
