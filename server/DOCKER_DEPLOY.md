# Docker Deployment Guide

Complete guide for deploying the CSGT Scraper API using Docker.

## 🚀 Quick Start

### 1. Build and Run with Docker Compose

```bash
# Build and start the container
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f csgt-api
```

The API will be available at `http://localhost:8000`

### 2. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Submit a test job
curl -X POST "http://localhost:8000/api/v1/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "license_plate": "59C136047",
    "vehicle_type": "xemay",
    "max_retries": 3
  }'
```

## 📦 Docker Commands

### Build Image

```bash
# Build image
docker build -t csgt-scraper-api .

# Build with custom tag
docker build -t csgt-scraper-api:v1.0.0 .

# Build without cache
docker build --no-cache -t csgt-scraper-api .
```

### Run Container

```bash
# Run container
docker run -d \
  --name csgt-api \
  -p 8000:8000 \
  csgt-scraper-api

# Run with environment variables
docker run -d \
  --name csgt-api \
  -p 8000:8000 \
  -e API_WORKERS=4 \
  -e DEFAULT_MAX_RETRIES=5 \
  csgt-scraper-api

# Run with volume mounts
docker run -d \
  --name csgt-api \
  -p 8000:8000 \
  -v $(pwd)/captcha_images:/app/captcha_images \
  -v $(pwd)/logs:/app/logs \
  csgt-scraper-api
```

### Container Management

```bash
# Stop container
docker stop csgt-api

# Start container
docker start csgt-api

# Restart container
docker restart csgt-api

# Remove container
docker rm csgt-api

# View logs
docker logs csgt-api
docker logs -f csgt-api  # Follow logs

# Execute command in container
docker exec -it csgt-api bash

# View container stats
docker stats csgt-api
```

## 🔧 Docker Compose Commands

### Basic Operations

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f csgt-api

# Rebuild and start
docker-compose up -d --build

# Stop and remove everything (including volumes)
docker-compose down -v
```

### Scaling (if needed)

```bash
# Scale to multiple instances
docker-compose up -d --scale csgt-api=3
```

### Check Status

```bash
# View running containers
docker-compose ps

# View resource usage
docker-compose top
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file for configuration:

```bash
# .env file
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=2
DEFAULT_MAX_RETRIES=3
DOWNLOAD_DELAY=2
LOG_LEVEL=info
```

Then reference in `docker-compose.yml`:

```yaml
services:
  csgt-api:
    env_file:
      - .env
```

### Custom Configuration

Edit `docker-compose.yml` to customize:

```yaml
services:
  csgt-api:
    environment:
      - API_WORKERS=4        # Increase workers
      - DEFAULT_MAX_RETRIES=5  # More retries
    ports:
      - "8080:8000"          # Custom port
    deploy:
      resources:
        limits:
          cpus: '4'           # More CPU
          memory: 4G          # More RAM
```

## 🌐 Production Deployment

### 1. With Nginx Reverse Proxy

Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream csgt_api {
        server csgt-api:8000;
    }

    server {
        listen 80;
        server_name your-domain.com;

        location / {
            proxy_pass http://csgt_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Timeouts for long-running jobs
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }
    }
}
```

Uncomment nginx section in `docker-compose.yml` and start:

```bash
docker-compose up -d
```

### 2. With SSL/HTTPS (Let's Encrypt)

```bash
# Install certbot
sudo apt-get install certbot

# Get certificate
sudo certbot certonly --standalone -d your-domain.com

# Update nginx.conf for SSL
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    
    # ... rest of config
}

# Copy certificates to project
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ./ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ./ssl/
```

### 3. With Redis for Job Queue

Uncomment redis section in `docker-compose.yml`:

```yaml
services:
  redis:
    image: redis:7-alpine
    # ... redis config
```

Then update `api.py` to use Redis instead of in-memory storage.

## 📊 Monitoring & Logging

### View Logs

```bash
# All logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Only API logs
docker-compose logs -f csgt-api

# Only errors
docker-compose logs -f | grep ERROR
```

### Health Monitoring

```bash
# Manual health check
curl http://localhost:8000/health

# Watch health status
watch -n 5 'curl -s http://localhost:8000/health | jq'

# Check container health
docker inspect --format='{{.State.Health.Status}}' csgt-api
```

### Resource Monitoring

```bash
# Real-time stats
docker stats csgt-api

# Container processes
docker top csgt-api
```

## 🔒 Security Best Practices

### 1. Use Secrets for Sensitive Data

Create `secrets.env`:

```bash
API_TOKEN=your-secret-token-here
DATABASE_URL=postgresql://user:pass@host/db
```

Add to `.gitignore`:

```bash
echo "secrets.env" >> .gitignore
```

Reference in compose:

```yaml
services:
  csgt-api:
    env_file:
      - secrets.env
```

### 2. Run as Non-Root User

Already configured in Dockerfile:

```dockerfile
USER appuser
```

### 3. Network Isolation

```yaml
networks:
  csgt-network:
    driver: bridge
    internal: true  # No external access
```

### 4. Read-Only Filesystem (Optional)

```yaml
services:
  csgt-api:
    read_only: true
    tmpfs:
      - /tmp
      - /app/captcha_images
```

## 🚀 Cloud Deployment

### AWS EC2

```bash
# 1. SSH to EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# 2. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 3. Install Docker Compose
sudo apt-get install docker-compose-plugin

# 4. Clone repository
git clone your-repo-url
cd scrappy

# 5. Start services
docker-compose up -d

# 6. Configure security group to allow port 8000
```

### AWS ECS/Fargate

```bash
# 1. Build and push to ECR
aws ecr create-repository --repository-name csgt-scraper-api
docker tag csgt-scraper-api:latest your-account.dkr.ecr.region.amazonaws.com/csgt-scraper-api:latest
docker push your-account.dkr.ecr.region.amazonaws.com/csgt-scraper-api:latest

# 2. Create ECS task definition
# 3. Create ECS service
# 4. Configure load balancer
```

### Google Cloud Run

```bash
# 1. Build and push to GCR
gcloud builds submit --tag gcr.io/your-project/csgt-scraper-api

# 2. Deploy to Cloud Run
gcloud run deploy csgt-scraper-api \
  --image gcr.io/your-project/csgt-scraper-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### DigitalOcean App Platform

```bash
# 1. Push to GitHub/GitLab
# 2. Connect repository in DO App Platform
# 3. Configure:
#    - Dockerfile path: ./Dockerfile
#    - Port: 8000
#    - Environment variables
# 4. Deploy
```

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs csgt-api

# Check if port is in use
lsof -i :8000
sudo netstat -tulpn | grep 8000

# Rebuild without cache
docker-compose build --no-cache
docker-compose up -d
```

### Permission Errors

```bash
# Fix ownership
sudo chown -R $USER:$USER captcha_images logs

# Or run with sudo (not recommended for production)
sudo docker-compose up -d
```

### OCR Not Working

```bash
# Verify Tesseract is installed in container
docker exec -it csgt-api tesseract --version

# Check captcha images
docker exec -it csgt-api ls -la captcha_images/
```

### High Memory Usage

```bash
# Check stats
docker stats csgt-api

# Reduce workers
# Edit docker-compose.yml: API_WORKERS=1

# Restart
docker-compose restart
```

## 📈 Performance Tuning

### Optimize for Production

1. **Increase Workers**
   ```yaml
   environment:
     - API_WORKERS=4
   ```

2. **Add Resource Limits**
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '4'
         memory: 4G
   ```

3. **Use Redis for Job Storage**
   - Uncomment redis service
   - Update api.py to use Redis

4. **Enable Caching**
   ```python
   # Add Redis caching for results
   ```

5. **Use Gunicorn**
   ```dockerfile
   CMD ["gunicorn", "api:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
   ```

## 📝 Maintenance

### Backup Data

```bash
# Backup captcha images
docker cp csgt-api:/app/captcha_images ./backup/captcha_images

# Backup logs
docker cp csgt-api:/app/logs ./backup/logs
```

### Update Application

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose up -d --build

# Or with zero downtime
docker-compose up -d --no-deps --build csgt-api
```

### Clean Up

```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Clean everything
docker system prune -a --volumes
```

## 📚 Additional Resources

- Docker Docs: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/docker/

---

**🎉 Your API is now containerized and ready for production!**

