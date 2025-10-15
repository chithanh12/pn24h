# Quick Start Guide - Frontend

This guide will help you get the frontend up and running quickly.

## Prerequisites

1. **Backend API must be running**
   ```bash
   # In the server folder
   cd ../server
   docker compose up -d
   
   # Verify API is running
   curl http://localhost:8000/health
   ```

2. **Node.js 18+ installed**
   ```bash
   node --version  # Should be v18 or higher
   ```

## Steps

### 1. Install Dependencies

```bash
npm install
```

This will install all required packages (Next.js, React, TypeScript, Tailwind CSS, etc.)

### 2. Configure Environment

The `.env.local` file should already be created with:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

If it doesn't exist, create it:
```bash
cp .env.example .env.local
```

### 3. Start Development Server

```bash
npm run dev
```

You should see:
```
  ▲ Next.js 15.5.5
  - Local:        http://localhost:3000
  - Network:      http://192.168.x.x:3000

 ✓ Starting...
 ✓ Ready in 2.3s
```

### 4. Open in Browser

Navigate to: http://localhost:3000

### 5. Test the Application

1. Enter a license plate: `59C136047`
2. Select vehicle type: `Xe máy`
3. Click "Tra cứu"
4. Wait 15-30 seconds for results

## What You Should See

### Search Form
- Clean, modern interface
- License plate input field
- Vehicle type dropdown
- Blue "Tra cứu" (Search) button

### During Search
- Blue status indicator
- "Đang tra cứu" (Searching...)
- Progress bar
- Loading spinner

### Results
- Red header if violations found
- Green message if no violations
- Detailed violation cards with:
  - License plate
  - Vehicle info
  - Violation time and location
  - Fine details
  - Payment status

## Common Issues

### Backend not running
**Error**: `Failed to fetch` or `Network error`

**Solution**:
```bash
cd ../server
docker compose up -d
curl http://localhost:8000/health
```

### Wrong API URL
**Error**: Connection refused

**Solution**: Check `.env.local`:
```bash
cat .env.local
# Should show: NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Port 3000 already in use
**Error**: `Port 3000 is already in use`

**Solution**: Use a different port:
```bash
PORT=3001 npm run dev
```

### Build errors
**Solution**: Clear cache and reinstall:
```bash
rm -rf .next node_modules
npm install
npm run dev
```

## Development Tips

### Hot Reload
The development server auto-reloads on file changes. Edit any file in `src/` and see instant updates.

### Component Locations
- **Search Form**: `src/components/SearchForm.tsx`
- **Results Display**: `src/components/ViolationResults.tsx`
- **Status Indicator**: `src/components/JobStatusIndicator.tsx`
- **Main Page**: `src/app/page.tsx`

### Styling
- Uses Tailwind CSS utility classes
- Dark mode supported automatically
- Responsive design (mobile, tablet, desktop)

### API Client
- Located in `src/lib/api.ts`
- All backend communication happens here
- Easy to extend with new endpoints

## Next Steps

- Customize colors in `tailwind.config.ts`
- Add new features in `src/components/`
- Deploy to Vercel (see README.md)

## Need Help?

- Check `README.md` for full documentation
- Review `../docs/design.md` for architecture
- See `../server/API_GUIDE.md` for API details

## Production Build

When ready to deploy:

```bash
# Build for production
npm run build

# Test production build locally
npm start

# Or deploy to Vercel
vercel
```

Enjoy! 🎉

