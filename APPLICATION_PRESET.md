# GOMORA Application Preset & Setup Guide

## 🎵 What is GOMORA?

GOMORA is a **full-stack music streaming platform** with:
- ✅ User Authentication (JWT)
- ✅ Music Library & Search
- ✅ Music Player
- ✅ Playlists Management
- ✅ Favorites System
- ✅ Responsive UI

---

## 🚀 Quick Fix for 404 Error

Your Heroku app can't find the code because **files weren't pushed to GitHub**.

### **Fix it NOW (5 minutes):**

```bash
# 1. Go to your GOMORA directory
cd GOMORA

# 2. Pull latest files from GitHub
git pull origin main

# 3. Make sure all files are there
ls -la  # Should show: Procfile, runtime.txt, backend/, index.html

# 4. Add & commit
git add .
git commit -m "Add deployment files"

# 5. Push to Heroku
git push heroku main

# 6. Rebuild app
heroku rebuild -a gomora-music-app

# 7. Initialize database
heroku run "python -c 'from app import db, app; app.app_context().push(); db.create_all()'" -a gomora-music-app

# 8. Check logs
heroku logs -a gomora-music-app --tail
```

### **Test it:**
```bash
curl https://gomora-music-app.herokuapp.com/api/health
```

Should return:
```json
{"status": "healthy", "message": "GOMORA API is running"}
```

If still 404, check:
```bash
# View deployment logs
heroku logs -a gomora-music-app --tail

# Restart app
heroku restart -a gomora-music-app
```

---

## 📁 Deployment Checklist

✅ Procfile - Heroku config
✅ runtime.txt - Python version (3.11.3)
✅ backend/app.py - Flask app
✅ backend/requirements.txt - Dependencies + gunicorn
✅ index.html - Frontend
✅ All files committed to GitHub
✅ Heroku app created
✅ PostgreSQL addon added
✅ Environment variables set
✅ Code pushed to Heroku
✅ Database initialized

---

## 🆘 Troubleshooting

### **Problem: 404 Not Found**
**Solution:** Files not pushed - run:
```bash
git push heroku main
heroku rebuild -a gomora-music-app
```

### **Problem: Application Error**
**Solution:** Check logs:
```bash
heroku logs -a gomora-music-app --tail
```

### **Problem: Database Connection Error**
**Solution:** Reinitialize:
```bash
heroku pg:reset DATABASE -a gomora-music-app
heroku run "python -c 'from app import db, app; app.app_context().push(); db.create_all()'" -a gomora-music-app
```

### **Problem: Missing Dependencies**
**Solution:** Update requirements.txt and redeploy:
```bash
cat backend/requirements.txt
git push heroku main
```

---

**Your app ID: cpt1::mfvd9-1783121534623-4d159044a072**

✅ Just run the 8-step fix above and you're LIVE! 🚀