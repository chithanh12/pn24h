# System Requirements

## Project Overview

Vietnamese Traffic Police Scraper is a full-stack web application that automates the process of checking traffic violations from the official Vietnamese traffic police website (https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html).

---

## Backend Requirements

### Functional Requirements

#### 1. Web Scraping Engine
- **FR-BE-001**: System shall scrape traffic violation data from csgt.vn website
- **FR-BE-002**: System shall support multiple vehicle types:
  - Car (oto/car)
  - Motorcycle (xemay/motorcycle)
  - Electric bike (xedapdien/electric_bike)
- **FR-BE-003**: System shall accept license plate number as input (Vietnamese format)
- **FR-BE-004**: System shall handle dynamic form submission via AJAX
- **FR-BE-005**: System shall maintain session state across requests using cookies

#### 2. Captcha Handling
- **FR-BE-006**: System shall automatically detect captcha images from the website
- **FR-BE-007**: System shall solve captchas using OCR (Optical Character Recognition)
- **FR-BE-008**: System shall support the following captcha preprocessing techniques:
  - Grayscale conversion
  - Contrast enhancement
  - Gray pixel removal (noise reduction)
  - Image sharpening
  - Median filtering
  - Image upscaling (2x)
  - Morphological erosion
  - Adaptive thresholding
  - Binary thresholding
- **FR-BE-009**: System shall use voting system across multiple OCR configurations for improved accuracy
- **FR-BE-010**: System shall restrict OCR character set to lowercase letters (a-z) and numbers (0-9)
- **FR-BE-011**: System shall retry failed captcha attempts (default: 3 retries)
- **FR-BE-012**: System shall save captcha images for debugging purposes

#### 3. Data Extraction
- **FR-BE-013**: System shall extract the following violation details:
  - License plate
  - Vehicle color
  - Vehicle type
  - Violation time
  - Violation location
  - Violation behavior/offense
  - Payment status
  - Detecting unit
- **FR-BE-014**: System shall parse HTML responses and AJAX JSON responses
- **FR-BE-015**: System shall handle multiple violations per license plate
- **FR-BE-016**: System shall handle "no violation found" scenarios

#### 4. REST API
- **FR-BE-017**: System shall provide RESTful API endpoints for:
  - Submit scraping job (POST /api/v1/scrape)
  - Get job status (GET /api/v1/jobs/{job_id})
  - List all jobs (GET /api/v1/jobs)
  - Get statistics (GET /api/v1/stats)
  - Delete job (DELETE /api/v1/jobs/{job_id})
  - Health check (GET /health)
- **FR-BE-018**: System shall support asynchronous job processing
- **FR-BE-019**: System shall track job status (pending, running, completed, failed)
- **FR-BE-020**: System shall store job results with timestamps
- **FR-BE-021**: System shall provide detailed error messages for failures
- **FR-BE-022**: API shall support CORS for frontend integration
- **FR-BE-023**: API shall return JSON formatted responses

#### 5. Job Management
- **FR-BE-024**: System shall assign unique job IDs to each scraping request
- **FR-BE-025**: System shall track job creation and completion timestamps
- **FR-BE-026**: System shall allow job deletion
- **FR-BE-027**: System shall provide job statistics (total, completed, failed)

### Non-Functional Requirements

#### 1. Performance
- **NFR-BE-001**: API response time shall be < 500ms (excluding scraping time)
- **NFR-BE-002**: Scraping operation shall complete within 30 seconds (average)
- **NFR-BE-003**: System shall support concurrent scraping jobs
- **NFR-BE-004**: System shall implement request delays to avoid overwhelming target website (default: 2s)

#### 2. Reliability
- **NFR-BE-005**: System shall achieve 70%+ captcha solving accuracy
- **NFR-BE-006**: System shall handle network errors gracefully
- **NFR-BE-007**: System shall handle invalid license plates gracefully
- **NFR-BE-008**: System shall automatically retry on transient failures
- **NFR-BE-009**: System uptime shall be 99%+ (with proper deployment)

#### 3. Scalability
- **NFR-BE-010**: System shall support horizontal scaling via containerization
- **NFR-BE-011**: System shall use background task processing for scraping jobs
- **NFR-BE-012**: System architecture shall support future Redis/database integration

#### 4. Security
- **NFR-BE-013**: System shall not expose internal implementation details in API responses
- **NFR-BE-014**: System shall validate all input parameters
- **NFR-BE-015**: System shall implement rate limiting (ready for production)
- **NFR-BE-016**: System shall log security-relevant events

#### 5. Maintainability
- **NFR-BE-017**: Code shall follow Python PEP 8 style guidelines
- **NFR-BE-018**: System shall have comprehensive logging for debugging
- **NFR-BE-019**: System shall be containerized using Docker
- **NFR-BE-020**: System shall have clear documentation (API docs, setup guides)

#### 6. Observability
- **NFR-BE-021**: System shall log all scraping attempts
- **NFR-BE-022**: System shall save captcha images for debugging
- **NFR-BE-023**: System shall provide health check endpoint
- **NFR-BE-024**: System shall track job statistics

### Technical Requirements

#### Technology Stack
- **Python**: 3.9+
- **Framework**: Scrapy 2.11+
- **API Framework**: FastAPI 0.104+
- **Web Server**: Uvicorn 0.24+
- **OCR Engine**: Tesseract 4.0+
- **Image Processing**: Pillow 10.0+, NumPy 1.24+, SciPy 1.10+
- **Containerization**: Docker, Docker Compose

#### Dependencies
```
scrapy>=2.11.0
Pillow>=10.0.0
pytesseract>=0.3.10
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
```

#### System Requirements
- **OS**: Linux (Ubuntu/Debian recommended)
- **RAM**: Minimum 512MB, Recommended 2GB
- **CPU**: Minimum 1 core, Recommended 2+ cores
- **Disk**: 1GB+ free space
- **Network**: Stable internet connection
- **External Dependency**: Tesseract OCR installed

---

## Frontend Requirements

### Functional Requirements

#### 1. User Interface
- **FR-FE-001**: System shall provide a modern, responsive web interface
- **FR-FE-002**: System shall support mobile, tablet, and desktop viewports
- **FR-FE-003**: System shall have a search form with fields:
  - License plate input (with validation)
  - Vehicle type selector (dropdown)
- **FR-FE-004**: System shall display search results in a clear, readable format
- **FR-FE-005**: System shall show loading indicators during scraping operations
- **FR-FE-006**: System shall display error messages for failed operations

#### 2. Search Functionality
- **FR-FE-007**: User shall be able to submit license plate search
- **FR-FE-008**: User shall be able to select vehicle type
- **FR-FE-009**: System shall validate license plate format before submission
- **FR-FE-010**: System shall poll job status after submission
- **FR-FE-011**: System shall display real-time job status updates

#### 3. Results Display
- **FR-FE-012**: System shall display violation details when found:
  - License plate (formatted)
  - Vehicle type and color
  - Violation date/time
  - Violation location (with map link if possible)
  - Violation description
  - Payment status
  - Detecting authority
- **FR-FE-013**: System shall display "No violations found" message when applicable
- **FR-FE-014**: System shall support displaying multiple violations per vehicle
- **FR-FE-015**: System shall allow exporting results (PDF/print)

#### 4. Job Management
- **FR-FE-016**: User shall be able to view search history
- **FR-FE-017**: User shall be able to delete previous searches
- **FR-FE-018**: System shall show job statistics (total searches, etc.)
- **FR-FE-019**: System shall cache recent search results for quick access

#### 5. User Experience
- **FR-FE-020**: System shall provide helpful error messages
- **FR-FE-021**: System shall show progress indicators for long operations
- **FR-FE-022**: System shall auto-format license plate input (add dashes)
- **FR-FE-023**: System shall remember user preferences (vehicle type)
- **FR-FE-024**: System shall provide example license plate formats
- **FR-FE-025**: System shall have a help/FAQ section

### Non-Functional Requirements

#### 1. Performance
- **NFR-FE-001**: Initial page load shall be < 2 seconds
- **NFR-FE-002**: UI interactions shall respond within 100ms
- **NFR-FE-003**: System shall implement optimistic UI updates
- **NFR-FE-004**: System shall use client-side caching for repeated requests

#### 2. Usability
- **NFR-FE-005**: Interface shall be intuitive and require no training
- **NFR-FE-006**: System shall follow Vietnamese UI/UX conventions
- **NFR-FE-007**: System shall support Vietnamese language
- **NFR-FE-008**: Text shall be readable with appropriate font sizes
- **NFR-FE-009**: Color contrast shall meet WCAG 2.1 AA standards

#### 3. Accessibility
- **NFR-FE-010**: System shall support keyboard navigation
- **NFR-FE-011**: System shall have proper ARIA labels
- **NFR-FE-012**: System shall support screen readers
- **NFR-FE-013**: Form fields shall have clear labels and error states

#### 4. Compatibility
- **NFR-FE-014**: System shall support modern browsers (Chrome, Firefox, Safari, Edge)
- **NFR-FE-015**: System shall support browser versions from last 2 years
- **NFR-FE-016**: System shall be responsive across devices (320px - 4K)
- **NFR-FE-017**: System shall work on iOS and Android mobile browsers

#### 5. Maintainability
- **NFR-FE-018**: Code shall follow TypeScript/React best practices
- **NFR-FE-019**: Components shall be reusable and modular
- **NFR-FE-020**: System shall have clear component documentation
- **NFR-FE-021**: Code shall be type-safe (TypeScript)

### Technical Requirements

#### Technology Stack (Planned)
- **Framework**: Next.js 14+ (with App Router)
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 3+
- **UI Components**: shadcn/ui or Material-UI
- **State Management**: React Context / Zustand
- **HTTP Client**: Axios or Fetch API
- **Form Handling**: React Hook Form + Zod validation
- **Date Formatting**: date-fns
- **Icons**: Lucide Icons or Heroicons

#### Dependencies (Planned)
```json
{
  "next": "^14.0.0",
  "react": "^18.0.0",
  "react-dom": "^18.0.0",
  "typescript": "^5.0.0",
  "tailwindcss": "^3.3.0",
  "axios": "^1.6.0",
  "react-hook-form": "^7.48.0",
  "zod": "^3.22.0",
  "zustand": "^4.4.0",
  "date-fns": "^2.30.0"
}
```

#### System Requirements
- **Node.js**: 18+ LTS
- **npm/yarn/pnpm**: Latest stable
- **Browser Requirements**: ESM support, ES2020+

---

## Integration Requirements

### API Integration
- **IR-001**: Frontend shall communicate with backend via REST API
- **IR-002**: Frontend shall handle API authentication (if implemented)
- **IR-003**: Frontend shall implement proper error handling for API failures
- **IR-004**: Frontend shall poll job status at appropriate intervals (2-3 seconds)
- **IR-005**: Frontend shall respect rate limits

### Data Format
- **IR-006**: All dates shall use ISO 8601 format
- **IR-007**: License plates shall follow Vietnamese format (e.g., 59C-136.47)
- **IR-008**: Vehicle types shall use standardized codes (oto, xemay, xedapdien)
- **IR-009**: Error responses shall include error codes and messages

### Configuration
- **IR-010**: Frontend shall support configurable API base URL
- **IR-011**: Frontend shall support environment-specific configurations (dev, staging, prod)
- **IR-012**: Backend API URL shall be configurable via environment variables

---

## Testing Requirements

### Backend Testing
- **TR-BE-001**: Unit tests for captcha solving functions
- **TR-BE-002**: Integration tests for API endpoints
- **TR-BE-003**: End-to-end tests for complete scraping flow
- **TR-BE-004**: Test coverage should be > 70%

### Frontend Testing
- **TR-FE-001**: Unit tests for utility functions
- **TR-FE-002**: Component tests for UI components
- **TR-FE-003**: Integration tests for API integration
- **TR-FE-004**: E2E tests for critical user flows
- **TR-FE-005**: Test coverage should be > 80%

---

## Deployment Requirements

### Backend Deployment
- **DR-BE-001**: System shall be deployable via Docker
- **DR-BE-002**: System shall support Docker Compose orchestration
- **DR-BE-003**: System shall support Nginx reverse proxy
- **DR-BE-004**: System shall have proper logging configuration
- **DR-BE-005**: System shall support environment variable configuration

### Frontend Deployment
- **DR-FE-001**: System shall be deployable as static site
- **DR-FE-002**: System shall support CDN deployment
- **DR-FE-003**: System shall have production build optimization
- **DR-FE-004**: System shall support environment-based configuration

---

## Future Enhancements (Optional)

### Backend
- Redis integration for job queue and caching
- Database integration (PostgreSQL) for persistent storage
- WebSocket support for real-time updates
- API authentication and rate limiting
- Admin dashboard for monitoring
- Multiple language support for API responses

### Frontend
- Vietnamese language localization
- Dark mode support
- Print/export to PDF functionality
- Search history with filters
- Notification system for completed jobs
- Google Maps integration for violation locations
- Payment tracking and reminders
- User accounts and saved searches
- Mobile app (React Native)

---

## Constraints and Assumptions

### Constraints
1. Target website (csgt.vn) may change structure without notice
2. Captcha solving accuracy limited by OCR capabilities
3. Scraping speed limited by website response time and rate limiting
4. No official API available from csgt.vn

### Assumptions
1. Target website remains accessible and functional
2. Captcha format remains consistent
3. Users have valid Vietnamese license plates
4. Internet connection is stable
5. Docker and required dependencies can be installed on target system

