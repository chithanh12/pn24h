# Client - Vietnamese Traffic Police Scraper Frontend

> **Status**: ✅ Functional

A modern Next.js frontend application for searching and displaying Vietnamese traffic violation data.

## Features

- ✅ Modern, responsive web interface
- ✅ Real-time violation search
- ✅ Automatic job status polling
- ✅ Beautiful violation results display
- ✅ Mobile-friendly design
- ✅ Dark mode support
- ✅ Vietnamese language interface
- ✅ Loading states and error handling

## Tech Stack

- **Framework**: Next.js 15.5+ with App Router
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 4
- **State Management**: React Hooks
- **API Client**: Fetch API
- **UI**: Custom components with Tailwind

## Project Structure

```
src/
├── app/                    # Next.js app router
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page
│   └── globals.css         # Global styles
├── components/             # React components
│   ├── SearchForm.tsx      # License plate search form
│   ├── ViolationResults.tsx # Results display
│   └── JobStatusIndicator.tsx # Status indicator
├── lib/                    # Utilities
│   ├── api.ts              # API client
│   ├── types.ts            # TypeScript types
│   └── utils.ts            # Helper functions
└── hooks/                  # Custom hooks
    └── useJobPolling.ts    # Job status polling
```

## Setup

### Prerequisites

- Node.js 18+ LTS
- Backend API running (see [../server](../server))

### Installation

```bash
# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Edit .env.local to set your backend API URL
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Development

```bash
# Run development server
npm run dev

# Open http://localhost:3000 in your browser
```

The development server supports hot reloading - changes will be reflected immediately.

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

## Environment Variables

Create a `.env.local` file with the following variables:

```bash
# Backend API URL (required)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production, set this to your deployed backend URL.

## Usage

1. **Start the backend API** (see [../server](../server))
2. **Start the frontend**:
   ```bash
   npm run dev
   ```
3. **Open http://localhost:3000**
4. **Enter a license plate** (e.g., `59C136047`)
5. **Select vehicle type** (Xe máy/Ô tô/Xe đạp điện)
6. **Click "Tra cứu"** and wait for results (15-30 seconds)

## API Integration

The frontend communicates with the backend API running at `NEXT_PUBLIC_API_URL`.

**Endpoints used:**
- `POST /api/v1/scrape` - Submit scraping job
- `GET /api/v1/jobs/{id}` - Poll job status (every 3 seconds)

See [../server/API_GUIDE.md](../server/API_GUIDE.md) for full API documentation.

## Components

### SearchForm
- License plate input with validation
- Vehicle type selector
- Real-time error feedback
- Loading states

### ViolationResults
- Clean, card-based layout
- Displays violation details:
  - License plate and vehicle info
  - Violation time and location
  - Violation behavior
  - Payment status
  - Detecting unit
- Handles "no violations" state

### JobStatusIndicator
- Visual status updates
- Progress indicators
- Error messages
- Animated loading states

## Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variable in Vercel dashboard
NEXT_PUBLIC_API_URL=https://your-backend-api.com
```

### Static Export

```bash
# Add to next.config.ts:
# output: 'export'

npm run build
# Deploy the 'out' directory to any static host (Netlify, GitHub Pages, etc.)
```

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Android)

## Troubleshooting

**API connection issues:**
- Check backend is running (`docker compose ps` in server folder)
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`
- Check browser console for CORS errors

**Build errors:**
- Clear Next.js cache: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules && npm install`

## License

MIT
