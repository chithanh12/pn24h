#!/usr/bin/env python3
"""
FastAPI wrapper for CSGT Scraper

This provides a REST API interface for the traffic violation scraper.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path
import uuid
import json
from enum import Enum

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from csgt_scraper.spiders.csgt_spider import CsgtSpider

# Job storage (in production, use Redis or database)
jobs: Dict[str, Dict[str, Any]] = {}

# FastAPI app
app = FastAPI(
    title="CSGT Traffic Violation Scraper API",
    description="API for checking traffic violations from Vietnamese traffic police website",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",  # Alternative port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VehicleType(str, Enum):
    """Vehicle type enumeration"""
    oto = "oto"
    car = "car"
    xemay = "xemay"
    motorcycle = "motorcycle"
    xedapdien = "xedapdien"
    electric_bike = "electric_bike"


class JobStatus(str, Enum):
    """Job status enumeration"""
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class ScrapeRequest(BaseModel):
    """Request model for scraping job"""
    license_plate: str = Field(..., description="License plate number (e.g., 59C136047)", min_length=1)
    vehicle_type: VehicleType = Field(default=VehicleType.xemay, description="Type of vehicle")
    max_retries: int = Field(default=3, description="Maximum captcha retry attempts", ge=1, le=10)
    
    class Config:
        schema_extra = {
            "example": {
                "license_plate": "59C136047",
                "vehicle_type": "xemay",
                "max_retries": 3
            }
        }


class JobResponse(BaseModel):
    """Response model for job submission"""
    job_id: str = Field(..., description="Unique job identifier")
    status: JobStatus = Field(..., description="Current job status")
    message: str = Field(..., description="Status message")
    created_at: str = Field(..., description="Job creation timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "job_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "pending",
                "message": "Job created successfully",
                "created_at": "2025-10-15T14:30:00"
            }
        }


class JobResult(BaseModel):
    """Response model for job result"""
    job_id: str
    status: JobStatus
    license_plate: str
    vehicle_type: str
    created_at: str
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


def run_scraper(job_id: str, license_plate: str, vehicle_type: str, max_retries: int):
    """
    Run the scraper in background
    
    Args:
        job_id: Unique job identifier
        license_plate: License plate to check
        vehicle_type: Type of vehicle
        max_retries: Maximum retry attempts
    """
    try:
        jobs[job_id]['status'] = 'running'
        
        # Output file for this job
        output_file = Path(f"results_{job_id}.json")
        
        # Configure and run scraper
        settings = get_project_settings()
        settings.set('FEEDS', {
            str(output_file): {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True,
            }
        })
        
        # Run spider
        process = CrawlerProcess(settings)
        process.crawl(
            CsgtSpider,
            license_plate=license_plate,
            vehicle_type=vehicle_type,
            max_retries=max_retries
        )
        process.start()
        
        # Read results
        if output_file.exists():
            with open(output_file, 'r', encoding='utf-8') as f:
                results = json.load(f)
            
            # Update job with results
            jobs[job_id]['status'] = 'completed'
            jobs[job_id]['completed_at'] = datetime.now().isoformat()
            jobs[job_id]['result'] = results[0] if results else None
            
            # Clean up output file
            output_file.unlink()
        else:
            jobs[job_id]['status'] = 'failed'
            jobs[job_id]['error'] = 'No results generated'
            
    except Exception as e:
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['error'] = str(e)
        jobs[job_id]['completed_at'] = datetime.now().isoformat()


@app.get("/", tags=["General"])
async def root():
    """API root endpoint with basic information"""
    return {
        "name": "CSGT Traffic Violation Scraper API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "scrape": "POST /api/v1/scrape - Submit scraping job",
            "status": "GET /api/v1/jobs/{job_id} - Get job status",
            "list_jobs": "GET /api/v1/jobs - List all jobs"
        }
    }


@app.get("/health", tags=["General"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/v1/scrape", response_model=JobResponse, tags=["Scraping"])
async def scrape_violation(request: ScrapeRequest, background_tasks: BackgroundTasks):
    """
    Submit a scraping job to check traffic violations
    
    This endpoint creates a background job that will scrape the CSGT website
    for violation information. Use the returned job_id to check status.
    """
    # Create unique job ID
    job_id = str(uuid.uuid4())
    
    # Initialize job
    jobs[job_id] = {
        'job_id': job_id,
        'status': 'pending',
        'license_plate': request.license_plate,
        'vehicle_type': request.vehicle_type.value,
        'max_retries': request.max_retries,
        'created_at': datetime.now().isoformat(),
        'completed_at': None,
        'result': None,
        'error': None
    }
    
    # Add scraping task to background
    background_tasks.add_task(
        run_scraper,
        job_id,
        request.license_plate,
        request.vehicle_type.value,
        request.max_retries
    )
    
    return JobResponse(
        job_id=job_id,
        status=JobStatus.pending,
        message="Job created successfully. Use job_id to check status.",
        created_at=jobs[job_id]['created_at']
    )


@app.get("/api/v1/jobs/{job_id}", response_model=JobResult, tags=["Jobs"])
async def get_job_status(job_id: str):
    """
    Get the status and result of a scraping job
    
    Returns the current status of the job and results if completed.
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobResult(**jobs[job_id])


@app.get("/api/v1/jobs", tags=["Jobs"])
async def list_jobs(
    status: Optional[JobStatus] = None,
    limit: int = 10,
    offset: int = 0
):
    """
    List all scraping jobs
    
    Optionally filter by status and paginate results.
    """
    # Filter by status if provided
    filtered_jobs = jobs.values()
    if status:
        filtered_jobs = [j for j in filtered_jobs if j['status'] == status.value]
    else:
        filtered_jobs = list(filtered_jobs)
    
    # Sort by created_at (newest first)
    filtered_jobs.sort(key=lambda x: x['created_at'], reverse=True)
    
    # Paginate
    paginated = filtered_jobs[offset:offset + limit]
    
    return {
        "total": len(filtered_jobs),
        "offset": offset,
        "limit": limit,
        "jobs": paginated
    }


@app.delete("/api/v1/jobs/{job_id}", tags=["Jobs"])
async def delete_job(job_id: str):
    """
    Delete a job from the system
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    del jobs[job_id]
    
    return {"message": f"Job {job_id} deleted successfully"}


@app.get("/api/v1/stats", tags=["Statistics"])
async def get_statistics():
    """
    Get scraping statistics
    """
    total = len(jobs)
    pending = sum(1 for j in jobs.values() if j['status'] == 'pending')
    running = sum(1 for j in jobs.values() if j['status'] == 'running')
    completed = sum(1 for j in jobs.values() if j['status'] == 'completed')
    failed = sum(1 for j in jobs.values() if j['status'] == 'failed')
    
    # Calculate success rate
    finished = completed + failed
    success_rate = (completed / finished * 100) if finished > 0 else 0
    
    return {
        "total_jobs": total,
        "pending": pending,
        "running": running,
        "completed": completed,
        "failed": failed,
        "success_rate": f"{success_rate:.1f}%"
    }


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("CSGT Scraper API")
    print("=" * 60)
    print("Starting server...")
    print("API Docs: http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

