# Vietnamese Traffic Police Scraper

A full-stack application for scraping and displaying traffic violation data from the Vietnamese traffic police website (csgt.vn).

## Project Structure

This is a monorepo containing both backend and frontend applications:

```
scrappy/
├── server/          # Backend API (Python/Scrapy/FastAPI)
│   ├── api.py
│   ├── csgt_scraper/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md
│
└── client/          # Frontend Web App (Next.js) - Coming Soon
    └── README.md
```

## Quick Start

### Backend (Server)

The backend is a FastAPI application that scrapes traffic violation data using Scrapy with advanced captcha solving.

```bash
cd server
docker compose up -d
```

API will be available at: http://localhost:8000

See [server/README.md](./server/README.md) for detailed documentation.

### Frontend (Client)

Coming soon - Next.js web interface for displaying violation data.

```bash
cd client
# Coming soon
```

## Features

- **Automated Captcha Solving**: Advanced OCR with multiple preprocessing techniques
- **REST API**: FastAPI-based API with job management
- **Dockerized**: Easy deployment with Docker and Docker Compose
- **Retry Mechanism**: Automatic retry on captcha failures
- **Session Management**: Proper cookie handling for reliable scraping

## Development

- **Backend**: Python 3.9+, Scrapy, FastAPI, Tesseract OCR
- **Frontend**: Next.js, React, TypeScript (planned)

## License

MIT

