# CSGT Scraper API Guide

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the API Server
```bash
python api.py
```

The API will start on `http://localhost:8000`

## 📚 API Documentation

Interactive API docs available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 Endpoints

### 1. Submit Scraping Job

**POST** `/api/v1/scrape`

Submit a new job to check traffic violations.

**Request Body:**
```json
{
  "license_plate": "59C136047",
  "vehicle_type": "xemay",
  "max_retries": 3
}
```

**Vehicle Types:**
- `oto` or `car` - Ô tô (Car)
- `xemay` or `motorcycle` - Xe máy (Motorcycle)
- `xedapdien` or `electric_bike` - Xe đạp điện

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Job created successfully",
  "created_at": "2025-10-15T14:30:00"
}
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "license_plate": "59C136047",
    "vehicle_type": "xemay",
    "max_retries": 3
  }'
```

**Example Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/scrape",
    json={
        "license_plate": "59C136047",
        "vehicle_type": "xemay",
        "max_retries": 3
    }
)

job = response.json()
print(f"Job ID: {job['job_id']}")
```

### 2. Get Job Status

**GET** `/api/v1/jobs/{job_id}`

Get the status and result of a scraping job.

**Response (Pending):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "license_plate": "59C136047",
  "vehicle_type": "xemay",
  "created_at": "2025-10-15T14:30:00",
  "completed_at": null,
  "result": null,
  "error": null
}
```

**Response (Completed):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "license_plate": "59C136047",
  "vehicle_type": "xemay",
  "created_at": "2025-10-15T14:30:00",
  "completed_at": "2025-10-15T14:30:15",
  "result": {
    "license_plate": "59C136047",
    "violation_found": true,
    "violation_details": [{
      "license_plate": "59C1-360.47",
      "vehicle_color": "Nền mầu trắng, chữ và số màu đen",
      "vehicle_type": "Xe máy",
      "violation_time": "16:39, 01/10/2025",
      "violation_location": "nguyễn du + cách mạng tháng 8...",
      "violation_behavior": "16824.7.7.a.03.Điều khiển xe đi trên vỉa hè",
      "payment_status": "Chưa xử phạt"
    }],
    "status": "success"
  },
  "error": null
}
```

**Example cURL:**
```bash
curl "http://localhost:8000/api/v1/jobs/550e8400-e29b-41d4-a716-446655440000"
```

**Example Python:**
```python
import requests
import time

# Submit job
response = requests.post("http://localhost:8000/api/v1/scrape", json={
    "license_plate": "59C136047",
    "vehicle_type": "xemay"
})
job_id = response.json()['job_id']

# Poll for results
while True:
    result = requests.get(f"http://localhost:8000/api/v1/jobs/{job_id}")
    data = result.json()
    
    if data['status'] in ['completed', 'failed']:
        print(data)
        break
    
    print(f"Status: {data['status']}")
    time.sleep(2)
```

### 3. List All Jobs

**GET** `/api/v1/jobs`

List all scraping jobs with optional filtering.

**Query Parameters:**
- `status` (optional): Filter by status (pending, running, completed, failed)
- `limit` (optional): Number of results per page (default: 10)
- `offset` (optional): Offset for pagination (default: 0)

**Response:**
```json
{
  "total": 25,
  "offset": 0,
  "limit": 10,
  "jobs": [
    {
      "job_id": "...",
      "status": "completed",
      "license_plate": "59C136047",
      "created_at": "2025-10-15T14:30:00"
    }
  ]
}
```

**Example:**
```bash
# Get all completed jobs
curl "http://localhost:8000/api/v1/jobs?status=completed&limit=20"
```

### 4. Delete Job

**DELETE** `/api/v1/jobs/{job_id}`

Delete a job from the system.

**Response:**
```json
{
  "message": "Job 550e8400-e29b-41d4-a716-446655440000 deleted successfully"
}
```

### 5. Get Statistics

**GET** `/api/v1/stats`

Get overall scraping statistics.

**Response:**
```json
{
  "total_jobs": 100,
  "pending": 5,
  "running": 2,
  "completed": 85,
  "failed": 8,
  "success_rate": "91.4%"
}
```

### 6. Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-15T14:30:00"
}
```

## 🔄 Complete Workflow Example

```python
import requests
import time

API_URL = "http://localhost:8000"

# 1. Submit scraping job
print("Submitting job...")
response = requests.post(f"{API_URL}/api/v1/scrape", json={
    "license_plate": "59C136047",
    "vehicle_type": "xemay",
    "max_retries": 3
})
job = response.json()
job_id = job['job_id']
print(f"✓ Job created: {job_id}")

# 2. Poll for completion
print("\nWaiting for results...")
max_attempts = 30  # 60 seconds max
attempts = 0

while attempts < max_attempts:
    result = requests.get(f"{API_URL}/api/v1/jobs/{job_id}")
    data = result.json()
    
    status = data['status']
    print(f"  Status: {status}")
    
    if status == 'completed':
        print("\n✓ Job completed successfully!")
        
        # Check if violations found
        if data['result']['violation_found']:
            print("\n⚠️  VIOLATIONS FOUND:")
            for violation in data['result']['violation_details']:
                print(f"  - Time: {violation['violation_time']}")
                print(f"  - Location: {violation['violation_location']}")
                print(f"  - Violation: {violation['violation_behavior']}")
                print(f"  - Status: {violation['payment_status']}")
        else:
            print("\n✓ No violations found")
        break
        
    elif status == 'failed':
        print(f"\n✗ Job failed: {data.get('error', 'Unknown error')}")
        break
    
    time.sleep(2)
    attempts += 1

if attempts >= max_attempts:
    print("\n⏱️  Timeout waiting for results")

# 3. Get statistics
stats = requests.get(f"{API_URL}/api/v1/stats").json()
print(f"\nAPI Statistics:")
print(f"  Total jobs: {stats['total_jobs']}")
print(f"  Success rate: {stats['success_rate']}")
```

## 🐳 Docker Deployment (Optional)

### Create Dockerfile
```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

EXPOSE 8000

CMD ["python", "api.py"]
```

### Build and Run
```bash
docker build -t csgt-api .
docker run -p 8000:8000 csgt-api
```

## ⚙️ Production Configuration

### Using Uvicorn Directly
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Gunicorn + Uvicorn Workers
```bash
gunicorn api:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Environment Variables
```bash
# Optional: Configure via environment
export API_HOST=0.0.0.0
export API_PORT=8000
export API_WORKERS=4
```

## 🔒 Security Considerations

### 1. Add Authentication
```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

@app.post("/api/v1/scrape")
async def scrape_violation(
    request: ScrapeRequest,
    background_tasks: BackgroundTasks,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Verify token
    if credentials.credentials != "your-secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    # ... rest of code
```

### 2. Add Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/v1/scrape")
@limiter.limit("10/minute")
async def scrape_violation(...):
    # ... code
```

### 3. Use CORS Middleware
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 Monitoring & Logging

### Add Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### Add Prometheus Metrics
```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

## 🐛 Troubleshooting

### API won't start
- Check if port 8000 is available
- Verify all dependencies are installed
- Check Tesseract is installed: `tesseract --version`

### Jobs stuck in "pending" or "running"
- Check scrapy logs
- Verify network connectivity to csgt.vn
- Check captcha images in `captcha_images/` folder

### High failure rate
- Increase `max_retries` parameter
- Check OCR accuracy in logs
- Consider manual captcha solving

## 💡 Tips

1. **Batch Processing**: Submit multiple jobs in parallel
2. **Caching**: Cache results for frequently checked plates
3. **Webhooks**: Implement callbacks when jobs complete
4. **Database**: Use PostgreSQL/MongoDB for production job storage
5. **Queue**: Use Celery + Redis for better job management

---

**Built with FastAPI + Scrapy**

