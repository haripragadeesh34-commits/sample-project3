# Python Flask Application with Jenkins and Kubernetes Deployment

A production-ready Python Flask application with complete CI/CD pipeline using Jenkins and Kubernetes orchestration.

## Project Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker container configuration
├── Jenkinsfile           # Jenkins CI/CD pipeline
├── k8s/                  # Kubernetes manifests
│   ├── namespace.yaml    # Kubernetes namespace
│   ├── deployment.yaml   # Deployment configuration
│   ├── service.yaml      # Service configuration
│   ├── hpa.yaml          # Horizontal Pod Autoscaler
│   ├── configmap.yaml    # ConfigMaps for configuration
│   ├── serviceaccount.yaml # RBAC configuration
│   └── ingress.yaml      # Ingress configuration
├── tests/                # Unit tests
├── .env.example          # Environment variables example
└── README.md             # This file
```

## Features

### Application Features
- **Flask REST API** with multiple endpoints
- **Health checks** for Kubernetes probes
- **Structured logging** and error handling
- **Environment-based configuration**

### DevOps Features
- **Docker containerization** with multi-stage builds
- **Security-focused** Dockerfile (non-root user, minimal dependencies)
- **Jenkins Pipeline** with complete CI/CD workflow
- **Kubernetes manifests** for production deployment
- **Auto-scaling** with Horizontal Pod Autoscaler
- **Service discovery** and load balancing
- **Rolling updates** with zero downtime
- **Resource management** and limits
- **Security context** and RBAC

## Prerequisites

- Python 3.11+
- Docker
- Kubernetes 1.24+
- Jenkins 2.400+
- kubectl configured with cluster access

## Local Development

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/haripragadeesh34-commits/sample-project3.git
   cd sample-project3
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pytest  # For testing
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`

### Testing

```bash
pytest tests/ -v
```

## API Endpoints

- **`GET /health`** - Health check (for Kubernetes liveness probe)
- **`GET /ready`** - Readiness check (for Kubernetes readiness probe)
- **`GET /api/hello`** - Hello World endpoint
- **`GET /api/status`** - Application status

## Docker

### Build Image

```bash
docker build -t python-flask-app:1.0.0 .
```

### Run Container

```bash
docker run -p 5000:5000 \
  -e ENV=production \
  -e APP_VERSION=1.0.0 \
  python-flask-app:1.0.0
```

## Jenkins Deployment

### Setup Jenkins

1. **Install required plugins:**
   - Docker Pipeline
   - Kubernetes plugin
   - GitHub integration

2. **Create Docker Hub credentials:**
   - Manage Jenkins → Manage Credentials
   - Add Docker Hub credentials with ID: `docker-hub-credentials`

3. **Configure Kubernetes cloud:**
   - Manage Jenkins → Configure System
   - Add Kubernetes cloud with your cluster details

4. **Create Pipeline Job:**
   - New Item → Pipeline
   - Pipeline script from SCM
   - Repository URL: `https://github.com/haripragadeesh34-commits/sample-project3.git`
   - Script Path: `Jenkinsfile`

### Jenkinsfile Stages

1. **Checkout** - Clone repository
2. **Build** - Install dependencies
3. **Test** - Run unit tests
4. **Build Docker Image** - Create Docker image
5. **Push to Registry** - Push to Docker Hub
6. **Deploy to Kubernetes** - Update Kubernetes deployment
7. **Verify Deployment** - Check rollout status

## Kubernetes Deployment

### Prerequisites

1. **Create namespace:**
   ```bash
   kubectl apply -f k8s/namespace.yaml
   ```

2. **Create service account and RBAC:**
   ```bash
   kubectl apply -f k8s/serviceaccount.yaml
   ```

3. **Create ConfigMaps:**
   ```bash
   kubectl apply -f k8s/configmap.yaml
   ```

### Deploy Application

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

### Optional: Setup Ingress

```bash
# Install NGINX Ingress Controller (if not already installed)
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install nginx-ingress ingress-nginx/ingress-nginx

# Apply Ingress
kubectl apply -f k8s/ingress.yaml
```

### Verify Deployment

```bash
# Check deployment status
kubectl get deployments -n python-app

# Check pods
kubectl get pods -n python-app -w

# Check service
kubectl get svc -n python-app

# View logs
kubectl logs -f deployment/python-flask-app -n python-app

# Port forward for local testing
kubectl port-forward svc/python-flask-app 8080:80 -n python-app
```

Visit `http://localhost:8080/api/hello` to test the application.

## Environment Variables

- `ENV` - Environment (development/production)
- `DEBUG` - Debug mode (True/False)
- `PORT` - Application port (default: 5000)
- `APP_VERSION` - Application version
- `LOG_LEVEL` - Logging level

## Health Checks

The application provides endpoints for Kubernetes probes:

### Liveness Probe
Checks if the application is still running.
```bash
curl http://localhost:5000/health
```

### Readiness Probe
Checks if the application is ready to serve traffic.
```bash
curl http://localhost:5000/ready
```

## Auto-Scaling

The application uses HorizontalPodAutoscaler (HPA) to automatically scale based on:
- CPU utilization (70% threshold)
- Memory utilization (80% threshold)

Min replicas: 2
Max replicas: 10

## Security Features

- **Non-root container user** (UID: 1000)
- **Read-only root filesystem**
- **Security context** with dropped capabilities
- **Resource limits** and requests
- **Service account** with minimal permissions
- **RBAC configuration** for pod access
- **Network policies** (optional - add as needed)

## Troubleshooting

### Pod won't start
```bash
# Check pod status
kubectl describe pod <pod-name> -n python-app

# View logs
kubectl logs <pod-name> -n python-app
```

### Service not accessible
```bash
# Check endpoints
kubectl get endpoints python-flask-app -n python-app

# Check service
kubectl describe svc python-flask-app -n python-app
```

### Jenkins build fails
1. Check Jenkins logs: `/var/log/jenkins/jenkins.log`
2. Verify Docker Hub credentials
3. Check Kubernetes cloud configuration
4. Verify kubeconfig access

## Performance Tuning

### Gunicorn Workers
- Current: 4 workers
- Adjust based on CPU cores: `(2 × CPU) + 1`

### Container Resources
Adjust in `k8s/deployment.yaml`:
- CPU requests: 100m
- Memory requests: 128Mi
- CPU limits: 500m
- Memory limits: 512Mi

## Production Checklist

- [ ] Update Docker registry credentials
- [ ] Configure custom domain in Ingress
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure monitoring (Prometheus/Grafana)
- [ ] Set up logging (ELK/Loki)
- [ ] Configure backup strategy
- [ ] Set resource quotas per namespace
- [ ] Implement network policies
- [ ] Enable pod security policies
- [ ] Configure rate limiting

## Contributing

1. Create a feature branch
2. Make your changes
3. Add/update tests
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please open a GitHub issue.

---

**Last Updated:** 2026-06-17
