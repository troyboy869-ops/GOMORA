# GOMORA

A modern music streaming platform built with Vue.js and Flask with Vercel Web Analytics.

## 🎵 Features

- ✅ Vue.js 3 + Vite Frontend with Vercel Analytics
- ✅ Flask REST API Backend
- ✅ User Authentication (JWT)
- ✅ Music Library & Search
- ✅ Playlists Management
- ✅ Favorites System
- ✅ Responsive UI
- ✅ Web Analytics (Vercel)

## 🚀 Quick Start

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the backend
python app.py
```

The API will be available at `http://localhost:5000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Build for Production

```bash
cd frontend
npm run build
```

The Flask backend will automatically serve the built frontend from the `dist` folder.

## 📊 Vercel Web Analytics

This project includes Vercel Web Analytics integration. To enable:

1. Deploy to Vercel
2. Enable Web Analytics in your Vercel dashboard (Settings → Analytics)
3. Analytics will automatically start tracking page views and performance

The analytics are integrated in `frontend/src/main.js` using the `@vercel/analytics` package.

## 🏗️ Project Structure

```
GOMORA/
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── App.vue         # Main Vue component
│   │   └── main.js         # Entry point (includes Vercel Analytics)
│   ├── index.html          # HTML template
│   ├── vite.config.js      # Vite configuration
│   └── package.json        # Node.js dependencies
├── vercel.json             # Vercel deployment configuration
└── README.md               # This file
```

## 🔧 API Endpoints

- `GET /api/health` - Health check
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user (requires JWT)
- `GET /api/music` - Get all music (paginated)
- `GET /api/music/<id>` - Get specific music
- `GET /api/music/search?q=<query>` - Search music
- `POST /api/music` - Add music (requires JWT)
- `GET /api/playlists` - Get user playlists (requires JWT)
- `POST /api/playlists` - Create playlist (requires JWT)
- And more...

## 🌐 Deployment

### Heroku Deployment

See `APPLICATION_PRESET.md` for Heroku deployment instructions.

### Vercel Deployment

1. Connect your GitHub repository to Vercel
2. Vercel will automatically detect the configuration from `vercel.json`
3. Set environment variables in Vercel dashboard
4. Deploy!

## 📝 Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://user:password@localhost:5432/gomora_db
JWT_SECRET_KEY=your_jwt_secret_key_here
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

## 📄 License

See `LICENSE` file for details.
