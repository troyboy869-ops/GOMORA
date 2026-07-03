#!/bin/bash
# Heroku Deployment Guide for GOMORA

echo "🎵 GOMORA - Heroku Deployment Setup"
echo "===================================="
echo ""

# Step 1: Install Heroku CLI
echo "Step 1: Install Heroku CLI"
echo "Visit: https://devcenter.heroku.com/articles/heroku-cli"
echo "Then run: heroku login"
echo ""
read -p "Press Enter after installing Heroku CLI and logging in..."

# Step 2: Create Heroku app
echo ""
echo "Step 2: Creating Heroku app..."
heroku create gomora-music-app

# Step 3: Add PostgreSQL addon
echo ""
echo "Step 3: Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:hobby-dev -a gomora-music-app

# Step 4: Set environment variables
echo ""
echo "Step 4: Setting environment variables..."
heroku config:set SECRET_KEY=$(openssl rand -hex 32) -a gomora-music-app
heroku config:set JWT_SECRET_KEY=$(openssl rand -hex 32) -a gomora-music-app
heroku config:set FLASK_ENV=production -a gomora-music-app

# Step 5: Deploy
echo ""
echo "Step 5: Deploying to Heroku..."
git push heroku main

# Step 6: Run migrations (create tables)
echo ""
echo "Step 6: Initializing database..."
heroku run "python -c 'from app import db, app; app.app_context().push(); db.create_all()'" -a gomora-music-app

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Your backend is live at:"
heroku apps:info gomora-music-app -a gomora-music-app | grep "Web URL"
