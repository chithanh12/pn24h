# System Design Document

## 1. Executive Summary

The Vietnamese Traffic Police Scraper is a full-stack web application designed to automate the retrieval of traffic violation data from the official Vietnamese traffic police website (csgt.vn). The system employs advanced web scraping techniques, intelligent captcha solving, and a modern REST API architecture to provide users with an efficient way to check traffic violations.

**Key Components:**
- Backend: Python-based scraper with FastAPI REST API
- Frontend: Next.js-based web interface (planned)
- Deployment: Dockerized microservices architecture

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │          Next.js Web Application (Frontend)               │  │
│  │  - React Components                                       │  │
│  │  - State Management                                       │  │
│  │  - API Client                                             │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS/REST API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                 Nginx Reverse Proxy                       │  │
│  │  - Load Balancing                                         │  │
│  │  - SSL Termination                                        │  │
│  │  - Request Routing                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              FastAPI Application Server                   │  │
│  │  - API Endpoints                                          │  │
│  │  - Job Management                                         │  │
│  │  - Background Task Processing                             │  │
│  │  - Request Validation                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Internal API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Scraping Layer                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  Scrapy Framework                         │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │         Spider Engine (CsgtSpider)                 │  │  │
│  │  │  - Session Management                              │  │  │
│  │  │  - Form Submission                                 │  │  │
│  │  │  - AJAX Handling                                   │  │  │
│  │  │  - Response Parsing                                │  │  │
│  │  │  - Retry Logic                                     │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │       Captcha Solver Module                        │  │  │
│  │  │  - Image Preprocessing                             │  │  │
│  │  │  - OCR Engine (Tesseract)                          │  │  │
│  │  │  - Voting System                                   │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP Requests
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      External Services                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         CSGT.vn Website (Target Website)                  │  │
│  │  - HTML Forms                                             │  │
│  │  - AJAX Endpoints                                         │  │
│  │  - Captcha Images                                         │  │
│  │  - Violation Data                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       Storage Layer                              │
│  ┌────────────────────┐  ┌──────────────────┐                   │
│  │   File System      │  │  In-Memory Store │                   │
│  │  - Captcha Images  │  │  - Job Queue     │                   │
│  │  - Logs            │  │  - Job Results   │                   │
│  └────────────────────┘  └──────────────────┘                   │
│                                                                   │
│  Future: Redis Cache, PostgreSQL Database                        │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Interaction Flow

```
User → Frontend → API Gateway (Nginx) → FastAPI → Scrapy → CSGT.vn
                                              ↓
                                        Captcha Solver
                                              ↓
                                         Tesseract OCR
                                              ↓
                                      Response Parser
                                              ↓
                                        Job Storage
                                              ↓
User ← Frontend ← API Response ← FastAPI ← Results
```

---

## 3. Component Design

### 3.1 Frontend (Client Layer)

#### Architecture: Next.js App Router with React

**Directory Structure:**
```
client/
├── src/
│   ├── app/                    # App Router pages
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   ├── search/
│   │   │   └── page.tsx        # Search page
│   │   └── history/
│   │       └── page.tsx        # Search history
│   ├── components/             # React components
│   │   ├── ui/                 # Base UI components
│   │   ├── SearchForm.tsx      # License plate search form
│   │   ├── ResultsDisplay.tsx  # Violation results display
│   │   ├── JobStatus.tsx       # Job status indicator
│   │   └── ViolationCard.tsx   # Individual violation card
│   ├── lib/                    # Utilities and helpers
│   │   ├── api.ts              # API client
│   │   ├── types.ts            # TypeScript types
│   │   └── utils.ts            # Helper functions
│   ├── hooks/                  # Custom React hooks
│   │   ├── useJobStatus.ts     # Job polling hook
│   │   └── useSearch.ts        # Search logic hook
│   └── store/                  # State management
│       └── searchStore.ts      # Search state (Zustand)
├── public/                     # Static assets
└── package.json
```

**Key Components:**

1. **SearchForm Component**
   - Input: License plate, vehicle type
   - Validation: Real-time format checking
   - Submit: Creates scraping job via API

2. **JobStatus Component**
   - Polling: Checks job status every 2-3 seconds
   - Display: Loading spinner, progress indicator
   - Transition: Auto-switches to results when complete

3. **ResultsDisplay Component**
   - Renders: Violation details in card layout
   - Actions: Export, share, new search
   - Empty state: "No violations found"

**State Management:**
- Local state for UI interactions
- Zustand store for search history and results cache
- React Context for theme and user preferences

### 3.2 Backend (Application Layer)

#### 3.2.1 FastAPI Application

**Architecture: Async REST API with Background Tasks**

**Directory Structure:**
```
server/
├── api.py                      # FastAPI application entry point
├── csgt_scraper/
│   ├── __init__.py
│   ├── settings.py             # Scrapy settings
│   ├── items.py                # Data models
│   ├── pipelines.py            # Data processing pipelines
│   ├── middlewares.py          # Custom middlewares
│   ├── spiders/
│   │   ├── __init__.py
│   │   └── csgt_spider.py      # Main spider
│   └── utils/
│       ├── __init__.py
│       └── captcha_solver.py   # OCR module
└── examples/                   # Usage examples
```

**API Endpoints:**

| Endpoint | Method | Purpose | Response |
|----------|--------|---------|----------|
| `/health` | GET | Health check | Status |
| `/api/v1/scrape` | POST | Submit job | Job ID |
| `/api/v1/jobs/{id}` | GET | Get job status | Job details |
| `/api/v1/jobs` | GET | List all jobs | Job list |
| `/api/v1/jobs/{id}` | DELETE | Delete job | Success |
| `/api/v1/stats` | GET | Get statistics | Stats |

**Data Models:**

```python
# Request Model
ScrapeRequest:
  - license_plate: str (required)
  - vehicle_type: VehicleType (required)
  - max_retries: int (optional, default: 3)

# Response Model
JobResponse:
  - job_id: UUID
  - status: JobStatus (pending/running/completed/failed)
  - license_plate: str
  - vehicle_type: str
  - created_at: datetime
  - completed_at: datetime (optional)
  - result: ViolationResult (optional)
  - error: str (optional)

# Violation Result
ViolationResult:
  - license_plate: str
  - vehicle_type: str
  - url: str
  - scraped_at: datetime
  - violation_found: bool
  - violation_details: List[ViolationDetail]
  - status: str

# Violation Detail
ViolationDetail:
  - license_plate: str
  - vehicle_color: str
  - vehicle_type: str
  - violation_time: str
  - violation_location: str
  - violation_behavior: str
  - payment_status: str
  - detecting_unit: str
```

**Background Task Processing:**
- Uses Python `concurrent.futures.ProcessPoolExecutor`
- Async job submission with immediate response
- Job status tracked in memory (dict)
- Future: Replace with Celery + Redis

#### 3.2.2 Scrapy Spider

**Architecture: Event-Driven Scraping Engine**

**Spider Workflow:**

```
1. start_requests()
   ├── Set cookiejar=1 for session
   └── Request main page

2. save_captcha()
   ├── Parse HTML response
   ├── Extract captcha image URL
   ├── Download captcha image
   ├── Save to captcha_images/
   └── Call solve_captcha()

3. solve_captcha()
   ├── Load captcha image
   ├── Apply preprocessing (12 configurations):
   │   ├── Grayscale
   │   ├── High contrast
   │   ├── Sharpened
   │   ├── Gray pixel removal (threshold 100, 80, 120)
   │   ├── Median filter + gray removal
   │   ├── Upscaled 2x
   │   ├── Morphological erosion
   │   ├── Adaptive thresholding
   │   └── Alternative PSM modes
   ├── Run Tesseract OCR on each
   ├── Voting system (most common result)
   └── Return captcha text + confidence

4. submit_form()
   ├── Build form data:
   │   ├── BienKS (license plate)
   │   ├── Xe (vehicle type code)
   │   ├── captcha (solved text)
   │   ├── ipClient (empty)
   │   └── cUrl (current page URL)
   ├── Submit AJAX POST request
   ├── Set X-Requested-With header
   └── Maintain cookiejar

5. parse_ajax_response()
   ├── Parse JSON response
   ├── Check for error (404 = captcha failed)
   ├── Extract redirect URL
   ├── Retry if failed and retries < max
   └── Follow redirect to results page

6. parse_results()
   ├── Parse HTML results page
   ├── Extract violation details using XPath
   ├── Handle multiple violations
   ├── Format and yield results
   └── Save debug HTML
```

**Session Management:**
- Cookie jar maintains session across requests
- Captcha is session-bound
- No intermediate page reloads
- Single session from start to finish

**Error Handling:**
- Network errors: Retry with exponential backoff
- Captcha failure: Automatic retry (max 3 times)
- Invalid license plate: Return error in results
- Parsing errors: Log and return empty results

#### 3.2.3 Captcha Solver

**Architecture: Multi-Strategy OCR with Voting**

**Image Preprocessing Pipeline:**

```
Input Image
    ├── Configuration 1: Original + PSM 7
    ├── Configuration 2: Grayscale + PSM 7
    ├── Configuration 3: High Contrast + PSM 8
    ├── Configuration 4: Sharpened + PSM 7
    ├── Configuration 5: Gray Removal (threshold=100) + PSM 7
    ├── Configuration 6: Gray Removal (threshold=80) + PSM 7
    ├── Configuration 7: Gray Removal (threshold=120) + PSM 7
    ├── Configuration 8: Median Filter + Gray Removal + PSM 7
    ├── Configuration 9: Upscaled 2x + PSM 7
    ├── Configuration 10: Morphological Erosion + PSM 7
    ├── Configuration 11: Adaptive Thresholding + PSM 7
    └── Configuration 12: Gray Removal + PSM 13
         ↓
    OCR Results Collection
         ↓
    Voting System (Counter)
         ↓
    Most Common Result + Confidence Score
         ↓
    Return to Spider
```

**Tesseract Configuration:**
- Character whitelist: `0123456789abcdefghijklmnopqrstuvwxyz`
- Page Segmentation Mode (PSM):
  - PSM 7: Single text line
  - PSM 8: Single word
  - PSM 13: Raw line
- Language: English (eng)
- OEM: LSTM only (--oem 1)

**Preprocessing Techniques:**

1. **Gray Pixel Removal**: Converts gray noise to white
   ```python
   pixels[pixels < threshold] = 255  # White
   pixels[pixels >= threshold] = 0    # Black
   ```

2. **Median Filter**: Removes salt-and-pepper noise
   ```python
   image.filter(ImageFilter.MedianFilter(size=3))
   ```

3. **Upscaling**: Improves recognition of small fonts
   ```python
   image.resize((width*2, height*2), Image.LANCZOS)
   ```

4. **Morphological Erosion**: Separates touching characters
   ```python
   scipy.ndimage.binary_erosion(binary_image, structure)
   ```

5. **Adaptive Thresholding**: Handles uneven lighting
   ```python
   block_size = 11
   threshold = mean(block) - C
   ```

**Accuracy Metrics:**
- Target: 70%+ success rate
- Current: ~60-70% (based on testing)
- Confidence scoring based on voting agreement

### 3.3 Deployment Layer

#### Docker Architecture

**Multi-Container Setup:**

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Host                           │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │         Docker Network (csgt-network)          │    │
│  │                                                  │    │
│  │  ┌──────────────────────────────────────────┐  │    │
│  │  │      Nginx Container (optional)          │  │    │
│  │  │  Port: 80, 443                           │  │    │
│  │  │  Volume: nginx.conf                      │  │    │
│  │  └──────────────────────────────────────────┘  │    │
│  │                    ↓                            │    │
│  │  ┌──────────────────────────────────────────┐  │    │
│  │  │      FastAPI Container (csgt-api)        │  │    │
│  │  │  Port: 8000                              │  │    │
│  │  │  Volumes:                                │  │    │
│  │  │    - ./captcha_images:/app/captcha_images│  │    │
│  │  │    - ./logs:/app/logs                    │  │    │
│  │  │  Resources: 2 CPU, 2GB RAM               │  │    │
│  │  └──────────────────────────────────────────┘  │    │
│  │                    ↓                            │    │
│  │  ┌──────────────────────────────────────────┐  │    │
│  │  │   Redis Container (optional, future)     │  │    │
│  │  │  Port: 6379                              │  │    │
│  │  │  Volume: redis-data                      │  │    │
│  │  └──────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

**Dockerfile Layers:**

```dockerfile
FROM python:3.9-slim-buster          # Base image
    ↓
Install system dependencies           # Tesseract, curl
    ↓
Set working directory /app
    ↓
Copy requirements.txt
    ↓
Install Python packages               # pip install
    ↓
Copy application code
    ↓
Expose port 8000
    ↓
Set entrypoint: uvicorn api:app
```

**Container Features:**
- Health checks every 30 seconds
- Auto-restart on failure
- Resource limits (CPU, memory)
- Volume persistence for data
- Logging with rotation (10MB, 3 files)

---

## 4. Data Flow

### 4.1 Complete Scraping Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  1. User submits search request                                 │
│     - License plate: 59C136047                                  │
│     - Vehicle type: xemay                                       │
└─────────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. Frontend sends POST /api/v1/scrape                          │
│     - Request body: {license_plate, vehicle_type}               │
└─────────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. FastAPI creates background job                              │
│     - Generate job_id: UUID                                     │
│     - Store in jobs dict: {job_id: {status: "pending", ...}}    │
│     - Return immediately: {job_id, status: "pending"}           │
└─────────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. Background task starts Scrapy spider                        │
│     - Update status: "running"                                  │
│     - Initialize CrawlerProcess                                 │
│     - Start CsgtSpider with parameters                          │
└─────────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│  5. Spider requests main page                                   │
│     - URL: https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html│
│     - Set cookiejar: 1                                          │
│     - Receive: HTML + session cookies                           │
└─────────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│  6. Spider extracts and downloads captcha                       │
│     - CSS selector: img#imgCaptcha::attr(src)                   │
│     - Download image                                            │
│     - Save: captcha_images/captcha_TIMESTAMP.png                │
└─────────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│  7. Captcha solver processes image                              │
│     - Load image with PIL                                       │
│     - Apply 12 preprocessing configurations                     │
│     - Run Tesseract OCR on each                                 │
│     - Collect results: ["abc123", "abc123", "abl23", ...]       │
│     - Vote: Most common = "abc123" (confidence: 9/12 = 75%)     │
└─────────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│  8. Spider submits form via AJAX                                │
│     - Endpoint: /?mod=contact&task=tracuu_post&ajax             │
│     - Method: POST                                              │
│     - Headers: X-Requested-With: XMLHttpRequest                 │
│     - Data: {BienKS, Xe, captcha, ipClient, cUrl}               │
│     - Maintain cookiejar                                        │
└─────────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│  9. CSGT server validates captcha                               │
│     - Check captcha against session                             │
│     - If valid: Return {href: "/tra-cuu-ket-qua?id=xxx"}        │
│     - If invalid: Return {status: 404}                          │
└─────────────────────────────────────────────────────────────────┘
                         ↓
            ┌────────────┴────────────┐
            │                         │
     Captcha Valid              Captcha Invalid
            │                         │
            ↓                         ↓
┌───────────────────────┐  ┌──────────────────────────┐
│ 10a. Follow redirect  │  │ 10b. Retry mechanism     │
│      to results page  │  │  - Increment retry_count │
│                       │  │  - If < max_retries:     │
│                       │  │    Go back to step 5     │
│                       │  │  - Else: Return error    │
└───────────────────────┘  └──────────────────────────┘
            │
            ↓
┌─────────────────────────────────────────────────────────────────┐
│  11. Parse results page HTML                                    │
│      - XPath selectors for violation data                       │
│      - Extract: license_plate, vehicle_color, violation_time... │
│      - Handle multiple violations                               │
│      - Format data structure                                    │
└─────────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│  12. Spider yields results                                      │
│      - ViolationResult object                                   │
│      - Status: "success" or "no_violations"                     │
│      - Timestamp: ISO 8601                                      │
└─────────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│  13. Background task completes                                  │
│      - Update job status: "completed"                           │
│      - Store results in jobs dict                               │
│      - Set completed_at timestamp                               │
└─────────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│  14. Frontend polls GET /api/v1/jobs/{job_id}                   │
│      - Every 2-3 seconds                                        │
│      - Detect status change to "completed"                      │
│      - Retrieve results                                         │
└─────────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│  15. Display results to user                                    │
│      - Violation details                                        │
│      - Location, time, fine amount                              │
│      - Export/share options                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Session Management Flow

```
Request 1: Initial Page Load
    ↓
Server sets cookies: PHPSESSID, session_id
    ↓
Scrapy stores in cookiejar=1
    ↓
Request 2: Captcha Image Download
    ↓
Send cookies from cookiejar=1
    ↓
Server associates captcha with session
    ↓
Request 3: Form Submission (AJAX)
    ↓
Send same cookies from cookiejar=1
    ↓
Server validates captcha against session
    ↓
Success: Session maintained throughout
```

---

## 5. Security Design

### 5.1 Input Validation
- License plate format validation (regex)
- Vehicle type enum restriction
- Parameter sanitization (XSS prevention)
- Request size limits

### 5.2 Rate Limiting
- API rate limiting (future: Redis-based)
- Request delay to target website (2 seconds)
- Max concurrent jobs limit
- Exponential backoff on errors

### 5.3 Error Handling
- No sensitive information in error messages
- Generic error responses to clients
- Detailed logging server-side only
- Graceful degradation

### 5.4 Data Privacy
- No user data storage (stateless)
- Job results cleared after retrieval
- Captcha images for debugging only (can be disabled)
- No logging of sensitive information

### 5.5 Infrastructure Security
- Docker container isolation
- Non-root user in containers
- Read-only file system (where possible)
- Environment-based secrets
- HTTPS/SSL (via Nginx)

---

## 6. Performance Optimization

### 6.1 Backend Optimization
- Background task processing (non-blocking API)
- Connection pooling
- Request caching (future: Redis)
- Efficient XPath selectors
- Image processing optimization

### 6.2 Frontend Optimization (Planned)
- Code splitting (Next.js automatic)
- Image optimization
- Client-side caching
- Debounced input validation
- Lazy loading components
- Service worker for offline support

### 6.3 Scraping Optimization
- Session reuse (cookiejar)
- Efficient CSS/XPath selectors
- Parallel OCR processing
- Image preprocessing optimization
- Smart retry strategy

---

## 7. Scalability Design

### 7.1 Horizontal Scaling

**Current State:**
- Single container deployment
- In-memory job storage
- Stateless API (mostly)

**Future State:**
```
Load Balancer (Nginx)
    ├── FastAPI Instance 1
    ├── FastAPI Instance 2
    └── FastAPI Instance N
         ↓
    Redis (Job Queue + Cache)
         ↓
    PostgreSQL (Persistent Storage)
```

### 7.2 Scaling Strategies

1. **API Layer Scaling:**
   - Multiple FastAPI instances behind load balancer
   - Shared state via Redis
   - Session affinity not required

2. **Scraping Layer Scaling:**
   - Distributed task queue (Celery)
   - Multiple worker processes
   - Job queue in Redis
   - Worker autoscaling based on queue size

3. **Storage Scaling:**
   - Redis for cache and job queue
   - PostgreSQL for persistent data
   - Object storage (S3) for captcha images
   - Database read replicas

### 7.3 Performance Targets

| Metric | Current | Target (Scaled) |
|--------|---------|-----------------|
| Concurrent jobs | 5-10 | 100+ |
| API response time | <500ms | <200ms |
| Scraping time | 15-30s | 10-20s |
| Throughput | 10 jobs/min | 100+ jobs/min |

---

## 8. Monitoring and Observability

### 8.1 Logging Strategy

**Log Levels:**
- ERROR: Captcha failures, network errors, parsing failures
- WARNING: Retries, slow responses, rate limit approaches
- INFO: Job lifecycle, scraping progress, API requests
- DEBUG: Detailed scraping steps, OCR details (development only)

**Log Destinations:**
- Console: Docker logs
- Files: /app/logs/ (rotated daily)
- Future: Centralized logging (ELK, Datadog)

### 8.2 Metrics Collection

**Key Metrics:**
- Job success/failure rate
- Average scraping time
- Captcha solving accuracy
- API response times
- Error rates by type
- Active jobs count
- Queue depth

**Future: Prometheus + Grafana**

### 8.3 Health Checks

- `/health` endpoint for liveness
- Container health checks (Docker)
- Dependency checks (Tesseract availability)
- Resource monitoring (CPU, memory)

---

## 9. Error Handling Strategy

### 9.1 Error Categories

1. **Network Errors:**
   - Connection timeout
   - DNS resolution failure
   - SSL/TLS errors
   - Strategy: Retry with exponential backoff

2. **Captcha Errors:**
   - OCR failure
   - Invalid captcha response
   - Session expiration
   - Strategy: Automatic retry (max 3 times)

3. **Parsing Errors:**
   - HTML structure changed
   - Missing elements
   - Unexpected response format
   - Strategy: Log error, return graceful failure

4. **Validation Errors:**
   - Invalid license plate format
   - Invalid vehicle type
   - Missing required parameters
   - Strategy: Return 400 Bad Request with details

5. **System Errors:**
   - Out of memory
   - Disk full
   - Tesseract not available
   - Strategy: Return 503 Service Unavailable

### 9.2 Error Response Format

```json
{
  "job_id": "uuid",
  "status": "failed",
  "error": "Captcha solving failed after 3 retries",
  "error_code": "CAPTCHA_FAILED",
  "error_details": {
    "attempts": 3,
    "last_error": "Invalid captcha response"
  },
  "timestamp": "2025-10-15T09:00:00Z"
}
```

---

## 10. Testing Strategy

### 10.1 Unit Testing
- Captcha solver functions
- API endpoint handlers
- Data validation logic
- XPath selectors

### 10.2 Integration Testing
- API → Scraper integration
- Scraper → Target website
- End-to-end scraping flow
- Error handling paths

### 10.3 Performance Testing
- Load testing (concurrent requests)
- Stress testing (resource limits)
- Captcha solving speed
- Memory leak detection

---

## 11. Deployment Architecture

### 11.1 Development Environment
```
Developer Machine
├── Python virtual environment
├── Local Scrapy execution
├── FastAPI development server
└── Next.js dev server (port 3000)
```

### 11.2 Production Environment
```
Cloud Provider (AWS/GCP/Azure)
├── Docker Host (EC2/Compute Engine/VM)
│   ├── Nginx Container (reverse proxy)
│   ├── FastAPI Container (auto-restart)
│   └── Redis Container (optional)
├── Object Storage (S3/GCS) for captcha images
├── Database (RDS/Cloud SQL) - optional
└── CDN (CloudFront/CloudFlare) for frontend
```

### 11.3 CI/CD Pipeline (Future)
```
Git Push
    ↓
GitHub Actions / GitLab CI
    ├── Run tests
    ├── Build Docker images
    ├── Push to registry (Docker Hub/ECR)
    └── Deploy to production
         ├── Pull latest images
         ├── Run migrations
         ├── Rolling update
         └── Health check
```

---

## 12. Future Enhancements

### 12.1 Phase 2: Enhanced Backend
- [ ] Redis integration for job queue
- [ ] PostgreSQL for persistent storage
- [ ] WebSocket support for real-time updates
- [ ] API authentication (JWT)
- [ ] Rate limiting (Redis-based)
- [ ] Admin dashboard

### 12.2 Phase 3: Advanced Features
- [ ] User accounts and saved searches
- [ ] Email/SMS notifications
- [ ] Payment reminders
- [ ] Historical data tracking
- [ ] Analytics dashboard
- [ ] Multi-language support

### 12.3 Phase 4: Mobile Apps
- [ ] React Native mobile app
- [ ] Push notifications
- [ ] Offline mode
- [ ] Location-based features

---

## 13. Technology Stack Summary

### Backend
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Language | Python | 3.9+ | Core language |
| Framework | Scrapy | 2.11+ | Web scraping |
| API | FastAPI | 0.104+ | REST API |
| Server | Uvicorn | 0.24+ | ASGI server |
| OCR | Tesseract | 4.0+ | Captcha solving |
| Image Processing | Pillow | 10.0+ | Image manipulation |
| Numerical | NumPy | 1.24+ | Array operations |
| Scientific | SciPy | 1.10+ | Morphological ops |

### Frontend (Planned)
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | Next.js | 14+ | React framework |
| Language | TypeScript | 5+ | Type safety |
| Styling | Tailwind CSS | 3+ | Utility-first CSS |
| State | Zustand | 4+ | State management |
| Forms | React Hook Form | 7+ | Form handling |
| Validation | Zod | 3+ | Schema validation |
| HTTP | Axios | 1.6+ | API client |

### Infrastructure
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Containers | Docker | Application packaging |
| Orchestration | Docker Compose | Multi-container management |
| Reverse Proxy | Nginx | Load balancing, SSL |
| Cache (Future) | Redis | Job queue, caching |
| Database (Future) | PostgreSQL | Persistent storage |

---

## 14. API Design Principles

### RESTful Design
- Resource-based URLs
- Standard HTTP methods
- Proper status codes
- JSON request/response
- Versioned API (v1)

### Response Standards
```json
// Success Response
{
  "job_id": "uuid",
  "status": "completed",
  "result": { ... },
  "timestamp": "ISO 8601"
}

// Error Response
{
  "error": "Human-readable message",
  "error_code": "MACHINE_READABLE_CODE",
  "details": { ... }
}
```

### Status Codes
- 200: Success
- 201: Created
- 400: Bad Request
- 404: Not Found
- 422: Validation Error
- 500: Internal Server Error
- 503: Service Unavailable

---

## 15. Conclusion

This system design provides a robust, scalable foundation for the Vietnamese Traffic Police Scraper application. The architecture follows industry best practices:

- **Separation of Concerns**: Clear boundaries between layers
- **Scalability**: Designed for easy horizontal scaling
- **Maintainability**: Modular, well-documented codebase
- **Reliability**: Error handling, retries, health checks
- **Performance**: Async processing, caching strategies
- **Security**: Input validation, rate limiting, container isolation

The current implementation (Phase 1) provides a solid MVP with room for growth through the planned enhancements in Phases 2-4.

