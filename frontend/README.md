# GOMORA Frontend

Vue.js frontend for the GOMORA music streaming platform with Vercel Web Analytics.

## Features

- ✅ Vue 3 + Vite
- ✅ Vercel Web Analytics integrated
- ✅ API proxy to Flask backend
- ✅ Responsive UI

## Development

```bash
# Install dependencies
npm install

# Start dev server (http://localhost:3000)
npm run dev

# Build for production
npm run build
```

## Vercel Analytics

Vercel Web Analytics is integrated via the `@vercel/analytics` package.

The analytics injection is done in `src/main.js`:

```javascript
import { inject } from '@vercel/analytics'
inject()
```

### To enable analytics:

1. Deploy the project to Vercel
2. Enable Web Analytics in your Vercel dashboard
3. Analytics will automatically start tracking page views

### Development Mode

Analytics works in development mode but won't send data to Vercel. It will log events to the console instead.

## Project Structure

```
frontend/
├── public/           # Static assets
├── src/
│   ├── App.vue      # Main app component
│   └── main.js      # Entry point (includes analytics)
├── index.html       # HTML template
├── vite.config.js   # Vite configuration
└── package.json     # Dependencies
```

## API Integration

The frontend connects to the Flask backend API running on port 5000. In development, Vite proxies `/api/*` requests to `http://localhost:5000`.
